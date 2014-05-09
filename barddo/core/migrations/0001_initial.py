# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from MySQLdb.cursors import Warning


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'CollectionUnit'
        db.create_table(u'core_collectionunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal(u'core', ['CollectionUnit'])

        # Adding model 'Collection'
        db.create_table(u'core_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CollectionUnit'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.BarddoUser'])),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Collection'])

        # Detect if application supports fulltext search on given backend
        if not db.dry_run and db.backend_name == "mysql":
            try:
                db.execute("CREATE FULLTEXT INDEX fix_core_collection ON core_collection (name, summary)")
            except Warning:
                pass
                #db.execute("CREATE FULLTEXT INDEX fix_core_collection_name ON core_collection (name, summary)")
                #db.execute("CREATE FULLTEXT INDEX fix_core_collection_summary ON core_collection (summary)")
        else:
            # Adding index on 'Collection', fields ['name', 'summary']
            db.create_index(u'core_collection', ['name', 'summary'])

        # Adding model 'Work'
        db.create_table(u'core_work', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Collection'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, db_index=True)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author_works',
                                                                             to=orm['accounts.BarddoUser'])),
            ('unit_count', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('total_pages', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'core', ['Work'])

        # Adding unique constraint on 'Work', fields ['collection', 'unit_count']
        db.create_unique(u'core_work', ['collection_id', 'unit_count'])

        # Detect if application supports fulltext search on given backend
        if not db.dry_run and db.backend_name == "mysql":
            try:
                db.execute("CREATE FULLTEXT INDEX fix_core_work ON core_work (title, summary)")
            except Warning:
                pass
                #db.execute("CREATE FULLTEXT INDEX fix_core_work_title ON core_work (title)")
                #db.execute("CREATE FULLTEXT INDEX fix_core_work_summary ON core_work (summary)")
        else:
            # Adding index on 'Work', fields ['title', 'summary']
            db.create_index(u'core_work', ['title', 'summary'])


    def backwards(self, orm):
        # Removing index on 'Work', fields ['title', 'summary']
        db.delete_index(u'core_work', ['title', 'summary'])

        # Removing unique constraint on 'Work', fields ['collection', 'unit_count']
        db.delete_unique(u'core_work', ['collection_id', 'unit_count'])

        # Removing index on 'Collection', fields ['name', 'summary']
        db.delete_index(u'core_collection', ['name', 'summary'])

        # Deleting model 'CollectionUnit'
        db.delete_table(u'core_collectionunit')

        # Deleting model 'Collection'
        db.delete_table(u'core_collection')

        # Deleting model 'Work'
        db.delete_table(u'core_work')


    models = {
        u'accounts.barddouser': {
            'Meta': {'object_name': 'BarddoUser', 'index_together': "[['username', 'first_name', 'last_name']]"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.collection': {
            'Meta': {'object_name': 'Collection', 'index_together': "[['name', 'summary']]"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BarddoUser']"}),
            'cover': (
                'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'start_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CollectionUnit']"})
        },
        u'core.collectionunit': {
            'Meta': {'object_name': 'CollectionUnit'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.work': {
            'Meta': {'unique_together': "(('collection', 'unit_count'),)", 'object_name': 'Work',
                     'index_together': "[['title', 'summary']]"},
            'author': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "'author_works'", 'to': u"orm['accounts.BarddoUser']"}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Collection']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'total_pages': ('django.db.models.fields.SmallIntegerField', [], {}),
            'unit_count': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['core']