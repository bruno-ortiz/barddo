# coding=utf-8
# TODO: remove this line, tests only
import os
from colorama import Fore
from similarity import find_similar_after_import
from utils import is_similar

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barddo.settings.mb_development")

import Queue
import threading
import time
import db.barddo as mb

from django.utils import timezone
from django.db import transaction


from core.models import Collection

import centraldemangas
import mangashost

centraldemangas.create_source()

importers = [
    {
        u"source": centraldemangas.create_source(),
        u"index": centraldemangas.IndexParser,
        u'manga': centraldemangas.MangaParser,
        u"pages": centraldemangas.PagesParser
    },

    {
        u"source": mangashost.create_source(),
        u"index": mangashost.IndexParser,
        u'manga': mangashost.MangaParser,
        u"pages": mangashost.PagesParser
    }
]


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
            except Exception, e:
                print "Error importing tags " + str(e)
            finally:
                self.queue.task_done()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url, idx = self.queue.get()

            try:
                # print "Fetching data from manga '{}'".format(url)
                parser = importers[idx][u"manga"]()
                source = importers[idx][u"source"]
                name, data = parser.extract_manga_data(url)

                author = mb.get_or_create_author(data['author'])
                tags = [t for t in data['tags']]
                collection, new_status, created, repeated = mb.get_or_create_collection(name, data['cover'], data['sinopse'], author, tags,
                                                         data['status'], tags_queue, source)

                # Only update if from the same source, otherwise it'll replicate chapter data
                if (not repeated) and (source.id == collection.source.id):

                    # Only update if not completed
                    if created or collection.status == Collection.STATUS_ONGOING:
                        need_to_update = False if new_status == collection.status else True
                        chapter_parser = importers[idx][u"pages"]()

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
                        print Fore.YELLOW + u"Ignoring '{}', it's complete...".format(name) + Fore.WHITE
                else:
                    print Fore.YELLOW + u"Ignoring '{}', already imported by {}...".format(name, collection.source.name)  + Fore.WHITE
            except Exception, e:
                print Fore.RED + u"Error loading manga '{}'".format(str(e)) + Fore.WHITE
            finally:
                self.queue.task_done()


def threaded_crawler(queue_size):
    print "Crawling mangas"
    start = time.time()

    # spawn a pool of threads, and pass them queue instance
    for i in range(queue_size):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    # populate queue with data
    for idx in xrange(len(importers)):
        index_parser = importers[idx]["index"]()
        for url in index_parser.get_manga_list():
            queue.put((url, idx))

    # wait on the queue until everything has been processed
    queue.join()

    print "Done importing... Starting to save tags..."

    # save tags
    t = ThreadTags(tags_queue)
    t.setDaemon(True)
    t.start()
    tags_queue.join()

    #print "Done creating tags... Starting do filter similar collections..."
    #find_similar_after_import()

    print "Elapsed Time: {} with {} threads".format(time.time() - start, queue_size)