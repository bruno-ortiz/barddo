import Queue
import threading
import time
import db.barddo as mb

from django.utils import timezone
from django.db import transaction

from core.models import Collection
from centraldemangas.pages_parser import PagesParser
from centraldemangas.index_parser import IndexParser
from centraldemangas.manga_parser import MangaParser


queue = Queue.Queue()


tags_queue = Queue.Queue()


class ThreadTags(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            collection, tags = self.queue.get()
            try:
                with transaction.atomic():
                    collection.tags.add(*tags)
                    collection.save()
            finally:
                self.queue.task_done()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()

            try:
                # print "Fetching data from manga '{}'".format(url)
                parser = MangaParser()
                name, data = parser.extract_manga_data(url)

                author = mb.get_or_create_author(data['author'])
                tags = [t for t in data['tags']]
                collection, new_status, created = mb.get_or_create_collection(name, data['cover'], data['sinopse'], author, tags,
                                                         data['status'], tags_queue)

                if created or collection.status == Collection.STATUS_ONGOING:
                    need_to_update = False if new_status == collection.status else True
                    chapter_parser = PagesParser()

                    for pos in xrange(len(data['chapters'])):
                        chapter_data = data['chapters'][pos]
                        chapter_title = chapter_data['name']
                        chapter_url = chapter_data['url']
                        work, created = mb.get_or_create_work(collection, author, chapter_title, pos)

                        if created:
                            pages = chapter_parser.parse_chapters_pages(chapter_url)
                            mb.create_pages_for_work(work, pages)
                            need_to_update = True

                    if need_to_update:
                        with transaction.atomic():
                            collection.status = new_status
                            collection.last_updated = timezone.now()
                            collection.save()
                else:
                    print "Ignoring '{}', it's complete...".format(name)
            finally:
                self.queue.task_done()


def threaded_crawler(queue_size):
    print "Crawling central de mangas"
    start = time.time()

    # spawn a pool of threads, and pass them queue instance
    for i in range(queue_size):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    # populate queue with data
    index_parser = IndexParser()
    for url in index_parser.get_manga_list():
        queue.put(url)

    # wait on the queue until everything has been processed
    queue.join()

    print "Done importing... Starting to save tags..."

    # save tags
    t = ThreadTags(tags_queue)
    t.setDaemon(True)
    t.start()
    tags_queue.join()

    print "Elapsed Time: {} with {} threads".format(time.time() - start, queue_size)
