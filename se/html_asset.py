# Copyright 2022-2023 Laurent Defert
#
#  This file is part of SOSSE.
#
# SOSSE is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# SOSSE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with SOSSE.
# If not, see <https://www.gnu.org/licenses/>.

import logging
import os

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models

logger = logging.getLogger('html_snapshot')


def remove_html_asset_file(fn):
    try:
        logger.debug('deleting %s', fn)
        os.unlink(fn)
    except OSError:
        # should not happen
        pass
    try:
        dn = os.path.dirname(fn)
        logger.debug('rmdir start %s', dn)
        while dn.startswith(settings.SOSSE_HTML_SNAPSHOT_DIR):
            logger.debug('rmdir %s', dn)
            os.rmdir(dn)
            dn = os.path.dirname(dn)
    except OSError:
        # ignore directory not empty errors
        pass


class HTMLAsset(models.Model):
    url = models.TextField()
    filename = models.TextField()
    ref_count = models.PositiveBigIntegerField(default=0)
    download_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    max_age = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('url', 'filename'),)

    def init_ref_count(self):
        # TODO: fix the race condition below
        max_ref_count = HTMLAsset.objects.filter(filename=self.filename).aggregate(models.Max('ref_count'))
        max_ref_count = max_ref_count.get('ref_count__max') or 0
        HTMLAsset.objects.filter(id=self.id).update(ref_count=max_ref_count)
        logger.debug('refcount initialized for %s', self.url)

    def increment_ref(self):
        count = HTMLAsset.objects.filter(filename=self.filename).update(ref_count=models.F('ref_count') + 1)
        logger.debug('%s refcount incremented for %s', count, self.filename)

    def update_values(self, **kwargs):
        HTMLAsset.objects.filter(id=self.id).update(**kwargs)

    @staticmethod
    def html_delete_url(url):
        from .document import sanitize_url
        url = sanitize_url(url, True, True)
        for asset in HTMLAsset.objects.filter(url=url):
            asset.html_delete()

    def html_delete(self):
        fn = settings.SOSSE_HTML_SNAPSHOT_DIR + self.filename
        try:
            content = open(fn, 'rb').read()
            assets = HTMLAsset.html_extract_assets(content)
            for asset in assets:
                HTMLAsset.remove_file_ref(asset)
        except OSError:
            pass

        self.remove_ref()

    def remove_ref(self):
        # TODO: fix the race condition below
        logger.debug('removing ref on url %s', self.url)
        HTMLAsset.remove_file_ref(self.filename)

    @staticmethod
    def remove_file_ref(filename):
        logger.debug('removing ref on %s', filename)
        # TODO: fix the race condition below
        HTMLAsset.objects.filter(filename=filename).update(ref_count=models.F('ref_count') - 1)
        refs_count = HTMLAsset.objects.filter(filename=filename, ref_count__gt=0).aggregate(models.Sum('ref_count'))
        refs_count = refs_count.get('ref_count__sum')

        # refs_count is None when HTMLAsset.objects.filter(...) returns an empty set
        if refs_count is None or refs_count <= 0:
            logger.debug('removing file %s', filename)
            remove_html_asset_file(settings.SOSSE_HTML_SNAPSHOT_DIR + filename)

        HTMLAsset.objects.filter(filename=filename, ref_count__lte=0).delete()

    @staticmethod
    def html_extract_assets(content):
        from .html_snapshot import css_parser
        assets = set()
        soup = BeautifulSoup(content, 'html5lib')
        for elem in soup.find_all(True):
            if elem.name == 'style':
                if elem.string:
                    assets |= css_parser().css_extract_assets(elem.string, False)

            if elem.attrs.get('style'):
                assets |= css_parser().css_extract_assets(elem.attrs['style'], True)

            if 'srcset' in elem.attrs:
                urls = elem.attrs['srcset'].strip()
                urls = urls.split(',')

                for url in urls:
                    url = url.strip()
                    if ' ' in url:
                        url, _ = url.split(' ', 1)

                    # unescape comma that were in HTMLSnapshot.handle_assets
                    url = url.replace('%2C', ',')

                    if url.startswith(settings.SOSSE_HTML_SNAPSHOT_URL):
                        assets.add(url[len(settings.SOSSE_HTML_SNAPSHOT_URL):])

            for attr in ('src', 'href'):
                if attr not in elem.attrs:
                    continue

                url = elem.attrs[attr]
                if url.startswith(settings.SOSSE_HTML_SNAPSHOT_URL):
                    filename = url[len(settings.SOSSE_HTML_SNAPSHOT_URL):]
                    assets.add(filename)

                    if url.endswith('.css'):
                        filename = settings.SOSSE_HTML_SNAPSHOT_DIR + filename
                        assets |= css_parser().css_extract_assets(open(filename).read(), False)

        return assets

    def add_refs_from_cache(self):
        from .html_snapshot import css_parser
        self.add_file_ref(self.filename)

        if '.' not in self.filename:
            return
        _, extension = self.filename.rsplit('.', 1)

        if extension not in ('css', 'htm', 'html'):
            return

        filename = settings.SOSSE_HTML_SNAPSHOT_DIR + self.filename
        with open(filename, 'rb') as f:
            content = f.read()

        if extension == 'css':
            assets = css_parser().css_extract_assets(content, False)
        else:
            assets = HTMLAsset.html_extract_assets(content)
        for asset in assets:
            HTMLAsset.remove_file_ref(asset)
