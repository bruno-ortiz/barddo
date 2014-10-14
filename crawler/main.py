import Queue
import threading
import time

from django.utils import timezone
from bs4 import BeautifulSoup
from django.db import transaction

from core.models import Collection
from fetch import extract_manga_data, get_html, should_parse, get_manga_pages, INITIAL_URL, BASE_URL, \
    parse_chapters_pages
import barddo_import as mb


queue = Queue.Queue()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()

            try:
                print "Fetching data from manga '{}'".format(url)
                name, data = extract_manga_data(url)

                author = mb.get_or_create_author(data['author'])
                tags = [t for t in data['tags']]
                collection = mb.get_or_create_collection(name, data['cover'], data['sinopse'], author, tags,
                                                         data['status'])

                if collection.status == Collection.STATUS_ONGOING:
                    need_to_update = False

                    for pos in xrange(len(data['chapters'])):
                        chapter_data = data['chapters'][pos]
                        chapter_title = chapter_data['name']
                        chapter_url = chapter_data['url']
                        work, created = mb.get_or_create_work(collection, author, chapter_title, pos)

                        if created:
                            pages = parse_chapters_pages(chapter_url)
                            mb.create_pages_for_work(work, pages)
                            need_to_update = True

                    if need_to_update:
                        with transaction.atomic():
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
    html = get_html(INITIAL_URL)
    soup = BeautifulSoup(html, 'lxml')
    all_pages = get_manga_pages(soup)

    for page in all_pages:
        url = BASE_URL.format(page)
        if should_parse(url):
            queue.put(url)

    # wait on the queue until everything has been processed
    queue.join()
    print "Elapsed Time: {} with {} threads".format(time.time() - start, queue_size)

# threaded_crawler(15)
