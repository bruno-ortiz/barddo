# coding=utf-8
# TODO: remove this line, tests only
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barddo.settings.mb_development")

#
from core.models import Collection
from utils import is_similar
import cPickle as pickle
import os

if __name__ == "__main__":
    slugs = Collection.objects.values_list('id', 'slug', "cover_url", flat=False).all()

    cur = 1
    total = len(slugs)

    if os.path.exists("similar.pickle"):
        print "Loading from disk..."
        final = pickle.load(open("similar.pickle", "rb"))
    else:
        print "Loading from network..."
        final = {}
        for id, name, cover in slugs:
            print "Parsing {}/{}\r".format(cur, total),
            cur += 1
            results = filter(lambda n: name != n[1] and is_similar(name, n[1], 0.8), slugs)
            if len(results) > 0:
                final[name] = (id, cover, results)

        pickle.dump(final, open("similar.pickle", "wb"))

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
    for name, results in filtered.items():
        id = results[0]
        cover = results[1]
        similar = results[2]

        print "-------------------------------------------------"
        print "{} - {} ({}) is similar to: ".format(id, name, cover)
        for n in similar:
            print  str(n[0]) + " - " + n[1] + ": " + n[2]

    print "Done, filtering valuable results..."