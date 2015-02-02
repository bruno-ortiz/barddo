# coding=utf-8
# TODO: remove this line, tests only
import os
from django.core.mail import mail_admins

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barddo.settings.mb_development")

#
from core.models import Collection, CollectionAlias
from utils import is_similar
import cPickle as pickle
import os


def find_similar_after_import():
    existing_slugs = Collection.objects.values_list('id', 'slug', "cover_url", flat=False).filter(enabled=True)
    new_slugs = Collection.objects.values_list('id', 'slug', "cover_url", flat=False).filter(enabled=False)

    cur = 1
    total = len(new_slugs)

    print "Loading from network..."
    final = {}
    for id, name, cover in new_slugs:
        print "Parsing {}/{}\r".format(cur, total),
        cur += 1
        results = filter(lambda n: name != n[1] and is_similar(name, n[1], 0.8), existing_slugs)
        if len(results) > 0:
            final[name] = (id, cover, results)

    # Parsing
    print "Done loading data"
    filtered = {}
    for name, results in final.items():
        id = results[0]
        cover = results[1]
        similar = results[2]

        # One 2 one
        if len(similar) == 1 and similar[0][1] in filtered:
            continue

        # Novel
        if len(similar) == 1 and similar[0][1] + "-novel" in filtered:
            continue

        filtered[name] = (id, cover, similar)

    print "Done filtering data"
    result_string = ""
    for name, results in filtered.items():
        id = results[0]
        cover = results[1]
        similar = results[2]

        result_string += "-------------------------------------------------\n"
        result_string += "{} - {} ({}) is similar to: ".format(id, name, cover) + '\n'
        for n in similar:
            result_string += str(n[0]) + " - " + n[1] + ": " + n[2] + "\n"

    subject = "Importacao de mangás possivelmente repetidos"
    body = "Os Mangas abaixo provavelmente estao repetidos, analise e remova da base se for o caso...\n\n"
    mail_admins(subject, body)

    print "Done, filtering valuable results..."


#
# def find_similar():
#     slugs = Collection.objects.values_list('id', 'slug', "cover_url", flat=False).all()
#
#     cur = 1
#     total = len(slugs)
#
#     if os.path.exists("similar.pickle"):
#         print "Loading from disk..."
#         final = pickle.load(open("similar.pickle", "rb"))
#     else:
#         print "Loading from network..."
#         final = {}
#         for id, name, cover in slugs:
#             print "Parsing {}/{}\r".format(cur, total),
#             cur += 1
#             results = filter(lambda n: name != n[1] and is_similar(name, n[1], 0.8), slugs)
#             if len(results) > 0:
#                 final[name] = (id, cover, results)
#
#         pickle.dump(final, open("similar.pickle", "wb"))
#
#     # Parsing
#     print "Done loading data"
#     filtered = {}
#     for name, results in final.items():
#         id = results[0]
#         cover = results[1]
#         similar = results[2]
#
#         # One 2 one
#         if len(similar) == 1 and similar[0][1] in filtered:
#             continue
#
#         # Novel
#         if len(similar) == 1 and similar[0][1] + "-novel" in filtered:
#             continue
#
#         filtered[name] = (id, cover, similar)
#
#     print "Done filtering data"
#     for name, results in filtered.items():
#         id = results[0]
#         cover = results[1]
#         similar = results[2]
#
#         print "-------------------------------------------------"
#         print "{} - {} ({}) is similar to: ".format(id, name, cover)
#         for n in similar:
#             print  str(n[0]) + " - " + n[1] + ": " + n[2]
#
#     print "Done, filtering valuable results..."
#
#
def import_similar():
    print "Importing repeated items"
    with open("repeated.txt") as f:
        lines = f.readlines()
        for line in lines:
            items = line.strip().split("|")
            id = items[0]
            keya = items[1]
            keyb = items[2]

            print "importing {} - {}/{}".format(id, keya, keyb)

            CollectionAlias.objects.get_or_create(slug=keya, collection_id=id)
            CollectionAlias.objects.get_or_create(slug=keyb, collection_id=id)
    print "Done"


if __name__ == "__main__":
    import_similar()