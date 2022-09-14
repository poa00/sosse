# Generated by Django 3.2.12 on 2022-09-11 21:55

import datetime
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import se.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t', models.DateTimeField()),
                ('doc_count', models.PositiveIntegerField()),
                ('queued_url', models.PositiveIntegerField()),
                ('indexing_speed', models.PositiveIntegerField(blank=True, null=True)),
                ('freq', models.CharField(choices=[('M', 'M'), ('D', 'D')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DomainSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browse_mode', models.CharField(choices=[('detect', 'Detect'), ('selenium', 'Selenium'), ('requests', 'Requests')], default='detect', max_length=10)),
                ('domain', models.TextField()),
                ('robots_status', models.CharField(choices=[('unknown', 'Unknown'), ('empty', 'Empty'), ('loaded', 'Loaded'), ('ignore', 'Ignore')], default='unknown', max_length=10)),
                ('robots_ua_hash', models.CharField(blank=True, default='', max_length=32)),
                ('robots_allow', models.TextField(blank=True, default='')),
                ('robots_disallow', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='FavIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(unique=True)),
                ('content', models.BinaryField(blank=True, null=True)),
                ('mimetype', models.CharField(blank=True, max_length=64, null=True)),
                ('missing', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchEngine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(blank=True, default='', max_length=32)),
                ('long_name', models.CharField(blank=True, default='', max_length=48)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('html_template', models.CharField(max_length=2048)),
                ('shortcut', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='UrlPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_regex', models.TextField(unique=True)),
                ('crawl_when', models.CharField(choices=[('always', 'Always'), ('depth', 'Depending on depth'), ('never', 'Never')], default='always', max_length=6)),
                ('default_browse_mode', models.CharField(choices=[('detect', 'Detect'), ('selenium', 'Selenium'), ('requests', 'Requests')], default='detect', max_length=8)),
                ('recrawl_mode', models.CharField(choices=[('none', 'No recrawl'), ('constant', 'Constant time'), ('adaptive', 'Adaptive')], default='adaptive', max_length=8)),
                ('recrawl_dt_min', models.DurationField(blank=True, default=datetime.timedelta(seconds=60), help_text='Min. time before recrawling a page', null=True)),
                ('recrawl_dt_max', models.DurationField(blank=True, default=datetime.timedelta(days=365), help_text='Max. time before recrawling a page', null=True)),
                ('crawl_depth', models.PositiveIntegerField(default=0)),
                ('store_extern_links', models.BooleanField(default=False)),
                ('keep_params', models.BooleanField(default=False)),
                ('hash_mode', models.CharField(choices=[('raw', 'Hash raw content'), ('no_numbers', 'Normalize numbers before')], default='no_numbers', max_length=10)),
                ('auth_login_url_re', models.TextField(blank=True, null=True)),
                ('auth_form_selector', models.TextField(blank=True, null=True)),
                ('auth_cookies', models.TextField(blank=True, default='')),
                ('take_screenshots', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_processed', models.PositiveIntegerField()),
                ('worker_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(unique=True)),
                ('normalized_url', models.TextField()),
                ('title', models.TextField()),
                ('normalized_title', models.TextField()),
                ('content', models.TextField()),
                ('normalized_content', models.TextField()),
                ('content_hash', models.CharField(blank=True, max_length=128, null=True)),
                ('vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('lang_iso_639_1', models.CharField(blank=True, max_length=6, null=True)),
                ('vector_lang', se.models.RegConfigField(default='simple')),
                ('robotstxt_rejected', models.BooleanField(default=False)),
                ('redirect_url', models.TextField(blank=True, null=True)),
                ('screenshot_file', models.CharField(blank=True, max_length=4096, null=True)),
                ('screenshot_count', models.PositiveIntegerField(blank=True, null=True)),
                ('crawl_first', models.DateTimeField(blank=True, null=True)),
                ('crawl_last', models.DateTimeField(blank=True, null=True)),
                ('crawl_next', models.DateTimeField(blank=True, null=True)),
                ('crawl_dt', models.DurationField(blank=True, null=True)),
                ('crawl_depth', models.PositiveIntegerField(default=0)),
                ('error', models.TextField(blank=True, default='')),
                ('error_hash', models.TextField(blank=True, default='')),
                ('worker_no', models.PositiveIntegerField(blank=True, null=True)),
                ('favicon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='se.favicon')),
            ],
        ),
        migrations.CreateModel(
            name='AuthField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
                ('url_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='se.urlpolicy')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('pos', models.PositiveIntegerField()),
                ('link_no', models.PositiveIntegerField()),
                ('extern_url', models.TextField(blank=True, null=True)),
                ('screen_pos', models.CharField(blank=True, max_length=64, null=True)),
                ('doc_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links_to', to='se.document')),
                ('doc_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_from', to='se.document')),
            ],
            options={
                'unique_together': {('doc_from', 'link_no')},
            },
        ),
        migrations.AddIndex(
            model_name='document',
            index=django.contrib.postgres.indexes.GinIndex(fields=['vector'], name='se_document_vector_efded7_gin'),
        ),
    ]