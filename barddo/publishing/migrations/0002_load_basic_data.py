# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):
    def forwards(self, orm):
        from django.core.management import call_command

        call_command("loaddata", "publishing_basic_data.json")

    def backwards(self, orm):
        pass

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
        u'publishing.country': {
            'Meta': {'object_name': 'Country'},
            'country_language': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'country_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'publishing.publishinghouse': {
            'Meta': {'object_name': 'PublishingHouse'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'collections': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': u"orm['core.Collection']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['publishing.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [],
                      {'related_name': "'publishing_group_owner'", 'to': u"orm['accounts.BarddoUser']"}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [],
                           {'blank': 'True', 'related_name': "'publishing_group'", 'null': 'True',
                            'symmetrical': 'False', 'to': u"orm['accounts.BarddoUser']"})
        }
    }

    complete_apps = ['publishing']
    symmetrical = True
