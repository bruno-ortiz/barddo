import cPickle as pickle
import os

from django.utils import timezone
from django.utils.text import slugify
from django.db import transaction

from core.models import Collection, Work, RemotePage
from accounts.models import BarddoUser


def get_or_create_work(collection, author, title, number):
    with transaction.atomic():
        return Work.objects.get_or_create(collection=collection, title=title, summary=title, author=author, unit_count=number,
                                          is_published=True,
                                          defaults={'total_pages': 0, 'publish_date': timezone.now(),
                                                    'cover_url': collection.cover_url})


def create_pages_for_work(work, pages):
    with transaction.atomic():
        RemotePage.objects.bulk_create([RemotePage(work=work, url=url, sequence=pages.index(url)) for url in pages])


def get_or_create_collection(title, cover_url, summary, author, tags, status, tags_queue):
    inner_status = Collection.STATUS_COMPLETED if status == u"Completo" else Collection.STATUS_ONGOING

    with transaction.atomic():
        collection, created = Collection.objects.get_or_create(name=title, author=author,
                                                               defaults={'start_date': timezone.now(),
                                                                         'status': Collection.STATUS_ONGOING,
                                                                         'summary': summary,
                                                                         'cover_url': cover_url
                                                                        })

    # Schedule for post saving
    if created:
        tags_queue.put((collection, tags))

    return collection, inner_status, created


def get_or_create_author(name):
    login = slugify(name if isinstance(name, unicode) else name.decode("UTF-8"))
    if ' ' in name:
        first, last = name.rsplit(' ', 1)
    else:
        first = name
        last = ''

    with transaction.atomic():
        return BarddoUser.objects.get_or_create(username=login, is_publisher=True, defaults={
            'first_name': first,
            'last_name': last,
        })[0]


# TO REMOVE
if __name__ == "__main__":
    print 'Loading file...'
    pickle_path = os.path.join(os.path.dirname(__file__), 'mangas.pickle')
    manga_data = pickle.load(open(pickle_path, 'rb'))

    current = 1
    total = len(manga_data)

    main_tags = []

    for title, data in manga_data.iteritems():
        print u"Importing {}/{}: '{}'\r".format(current, total, title),

        author = get_or_create_author(data['author'])
        tags = [t for t in data['tags']]
        status = data['status']
        collection = get_or_create_collection(title, data['cover'], data['sinopse'], author, tags, status)

        for pos in xrange(len(data['chapters'])):
            chapter_data = data['chapters'][pos]
            chapter_title = chapter_data['name']
            chapter_url = chapter_data['url']
            work, created = get_or_create_work(collection, author, chapter_title, pos)

            if created:
                create_pages_for_work(work, chapter_data['pages'])
        current += 1

    print "Done!"