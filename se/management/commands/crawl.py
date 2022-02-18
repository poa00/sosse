import uuid
from multiprocessing import cpu_count, Process
from time import sleep

from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from ...models import UrlQueue, Document


class Command(BaseCommand):
    help = 'Crawl web pages'

    def add_arguments(self, parser):
        parser.add_argument('--once', action='store_true', help='Exit when url queue is empty')
        parser.add_argument('--requeue', action='store_true', help='Exit when url queue is empty')
        parser.add_argument('--force', action='store_true', help='Reindex url in error')
        parser.add_argument('--worker', nargs=1, type=int, default=[None], help='Worker count (defaults to the available cpu count * 2)')
        parser.add_argument('urls', nargs='*', type=str)


    @staticmethod
    def process(crawl_id, worker_no, options):
        connection.close()
        connection.connect()

        sleep_count = 0
        while True:
            if UrlQueue.crawl(worker_no, crawl_id):
                sleep_count = 0
            else:
                if options['once'] and UrlQueue.objects.count() == 0:
                    break
                if sleep_count == 0:
                    print('%s Idle...' % worker_no)
                sleep_count += 1
                if sleep_count == 60:
                    sleep_count = 0
                sleep(1)

    def handle(self, *args, **options):
        UrlQueue.objects.update(worker_no=None)

        for url in options['urls']:
            UrlQueue.queue(url=url)
        
        if options['requeue']:
            urls = Document.objects.values_list('url', flat=True)
            self.stdout.write('Queuing %i url...' % len(urls))
            for url in urls:
                UrlQueue.queue(url=url)

        if options['force']:
            UrlQueue.objects.update(error='', error_hash='')

        self.stdout.write('Crawl starting')
        crawl_id = uuid.uuid4()

        worker_count = options['worker'][0]
        if worker_count is None:
            worker_count = cpu_count() * 2

        workers = []
        for crawler_no in range(worker_count):
            p = Process(target=self.process, args=(crawl_id, crawler_no, options))
            p.start()
            workers.append(p)

        for worker in workers:
            worker.join()

        self.stdout.write('Crawl finished')
