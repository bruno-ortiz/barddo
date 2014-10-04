import cPickle as pickle
import os

from django.utils import timezone

# TODO: remove this line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barddo.settings.development")

from core.models import Collection, Work, RemotePage
from accounts.models import BarddoUser
from django.utils.text import slugify


def get_or_create_work(collection, author, title, number, pages):
    work, created = Work.objects.get_or_create(collection=collection, title=title, summary=title,
                                               cover_url=collection.cover_url, author=author, unit_count=number,
                                               is_published=True,
                                               defaults={'total_pages': len(pages), 'publish_date': timezone.now()})

    # TODO: check if there's any page change, and update
    if created:
        RemotePage.objects.bulk_create([RemotePage(work=work, url=url, sequence=pages.index(url)) for url in pages])


def get_or_create_collection(title, cover_url, summary, author, tags):
    collection, created = Collection.objects.get_or_create(name=title, summary=summary, cover_url=cover_url,
                                                           author=author, defaults={'start_date': timezone.now()})

    if created:
        collection.tags.add(*tags)
        collection.save()

    return collection


def get_or_create_author(name):
    login = slugify(name if isinstance(name, unicode) else name.decode("UTF-8"))
    if ' ' in name:
        first, last = name.rsplit(' ', 1)
    else:
        first = name
        last = ''

    return BarddoUser.objects.get_or_create(username=login, first_name=first, last_name=last, is_publisher=True)[0]


if __name__ == "__main__":
    print 'Loading file...'
    pickle_path = os.path.join(os.path.dirname(__file__), 'mangas.pickle')
    manga_data = pickle.load(open(pickle_path, 'rb'))

    result_sql = []
    chapters_sql = []
    tags_sql = []

    current = 1
    total = len(manga_data)

    main_tags = []

    for title, data in manga_data.iteritems():
        print u"Importing {}/{}: '{}'\r".format(current, total, title),

        author = get_or_create_author(data['author'])
        tags = [t for t in data['tags']]
        collection = get_or_create_collection(title, data['cover'], data['sinopse'], author, tags=tags)

        for pos in xrange(len(data['chapters'])):
            chapter_data = data['chapters'][pos]
            chapter_title = chapter_data['name']
            get_or_create_work(collection, author, chapter_title, pos, chapter_data['pages'])
        current += 1

    print "Done!"