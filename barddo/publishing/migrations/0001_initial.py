# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'publishing_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('country_language', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'publishing', ['Country'])

        # Adding model 'PublishingHouse'
        db.create_table(u'publishing_publishinghouse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('info', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publishing.Country'])),
            ('collections', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Collection'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publishing_group_owner', to=orm['accounts.BarddoUser'])),
        ))
        db.send_create_signal(u'publishing', ['PublishingHouse'])

        # Adding M2M table for field publishers on 'PublishingHouse'
        m2m_table_name = db.shorten_name(u'publishing_publishinghouse_publishers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publishinghouse', models.ForeignKey(orm[u'publishing.publishinghouse'], null=False)),
            ('barddouser', models.ForeignKey(orm[u'accounts.barddouser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['publishinghouse_id', 'barddouser_id'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'publishing_country')

        # Deleting model 'PublishingHouse'
        db.delete_table(u'publishing_publishinghouse')

        # Removing M2M table for field publishers on 'PublishingHouse'
        db.delete_table(db.shorten_name(u'publishing_publishinghouse_publishers'))


    models = {
        u'accounts.barddouser': {
            'Meta': {'object_name': 'BarddoUser', 'index_together': "[['username', 'first_name', 'last_name']]"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.collection': {
            'Meta': {'object_name': 'Collection', 'index_together': "[['name', 'summary']]"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BarddoUser']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'collections': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Collection']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['publishing.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publishing_group_owner'", 'to': u"orm['accounts.BarddoUser']"}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publishing_group'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.BarddoUser']"})
        }
    }

    complete_apps = ['publishing']