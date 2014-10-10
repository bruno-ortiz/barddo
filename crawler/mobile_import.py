from core.models import Collection
from django.utils import timezone

SQL_INSERT_MANGA = "INSERT INTO manga (_id, title, cover, author, summary, favourite) VALUES ({}, '{}', '{}','{}', '{}', 0);"
SQL_INSERT_TAGS = "INSERT INTO tags (_id, name) VALUES ({}, '{}');"
SQL_RELATE_MANGA_TAGS = 'INSERT INTO manga_tags (manga_id, tag_id) VALUES ({}, {});'
SQL_INSERT_CHAPTER = "INSERT INTO manga_chapter (manga_id, _id, read) VALUES ({}, {}, 0);"


def import_to_mobile():
    result_sql = []
    chapters_sql = []
    tags_sql = []

    current = 1
    all_mangas = Collection.objects.select_related("author").prefetch_related("tags").all()
    total = len(all_mangas)
    parsed_tags = []

    for manga in all_mangas:
        print "Importing {}/{}: '{}'".format(current, total, manga.name)

        # Manga data
        result_sql.append(
            SQL_INSERT_MANGA.format(manga.id, manga.name.encode("UTF-8").replace("'", "''"), manga.cover_url,
                                    manga.author.get_full_name().encode("UTF-8").replace("'", "''"),
                                    manga.summary.encode("UTF-8").replace("'", "''").replace('\n', " ")))

        # Tags
        for tag in manga.tags.all():
            result_sql.append(SQL_RELATE_MANGA_TAGS.format(manga.id, tag.id))

            # Insert on main list
            if tag.id not in parsed_tags:
                parsed_tags.append(tag.id)
                tags_sql.append(SQL_INSERT_TAGS.format(tag.id, tag.name.encode("UTF-8").replace("'", "''")))

        # Chapters
        for chapter in manga.works.all():
            chapters_sql.append(SQL_INSERT_CHAPTER.format(manga.id, chapter.id))

        result_sql.append('')
        current += 1

    with open('mobile_database.sql', 'w') as output:
        output.write("CREATE TABLE manga (_id INT, title TEXT, cover TEXT,  author TEXT, summary TEXT, favourite BOOLEAN);\n")
        output.write("CREATE TABLE manga_tags (manga_id INT, tag_id INT);\n")
        output.write("CREATE TABLE manga_chapter (manga_id INT, _id INT, read BOOLEAN);\n")
        output.write("CREATE TABLE manga_chapter_page (chapter_id INT, position INT, url TEXT);\n")
        output.write("CREATE TABLE tags (_id INT, name TEXT);\n")
        output.write("CREATE TABLE last_updated (updated TEXT);\n")

        output.write("BEGIN;\n")
        output.write("\n".join(tags_sql))
        output.write("\n".join(result_sql))
        output.write("\n".join(chapters_sql))
        output.write("\nINSERT INTO last_updated (updated) VALUES ('{}');".format(timezone.now().__str__()))
        output.write("\nCOMMIT;")

    print "Done!"
