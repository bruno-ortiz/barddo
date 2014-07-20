# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentMethod'
        db.create_table(u'payments_paymentmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'payments', ['PaymentMethod'])

        # Adding model 'Payment'
        db.create_table(u'payments_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('settled_date', self.gf('django.db.models.fields.DateField')(null=True, db_index=True)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.PaymentMethod'])),
        ))
        db.send_create_signal(u'payments', ['Payment'])

        # Adding model 'PurchaseStatus'
        db.create_table(u'payments_purchasestatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'payments', ['PurchaseStatus'])

        # Adding model 'Purchase'
        db.create_table(u'payments_purchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('payment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['payments.Payment'], unique=True, null=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.BarddoUser'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payments.PurchaseStatus'])),
        ))
        db.send_create_signal(u'payments', ['Purchase'])

        # Adding model 'Item'
        db.create_table(u'payments_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['payments.Purchase'])),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Work'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'payments', ['Item'])

        # Adding unique constraint on 'Item', fields ['purchase', 'work']
        db.create_unique(u'payments_item', ['purchase_id', 'work_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Item', fields ['purchase', 'work']
        db.delete_unique(u'payments_item', ['purchase_id', 'work_id'])

        # Deleting model 'PaymentMethod'
        db.delete_table(u'payments_paymentmethod')

        # Deleting model 'Payment'
        db.delete_table(u'payments_payment')

        # Deleting model 'PurchaseStatus'
        db.delete_table(u'payments_purchasestatus')

        # Deleting model 'Purchase'
        db.delete_table(u'payments_purchase')

        # Deleting model 'Item'
        db.delete_table(u'payments_item')


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
        u'core.work': {
            'Meta': {'unique_together': "(('collection', 'unit_count'),)", 'object_name': 'Work', 'index_together': "[['title', 'summary']]"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author_works'", 'to': u"orm['accounts.BarddoUser']"}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Collection']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2', 'db_index': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'total_pages': ('django.db.models.fields.SmallIntegerField', [], {}),
            'unit_count': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'payments.item': {
            'Meta': {'unique_together': "(('purchase', 'work'),)", 'object_name': 'Item'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['payments.Purchase']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Work']"})
        },
        u'payments.payment': {
            'Meta': {'object_name': 'Payment'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.PaymentMethod']"}),
            'settled_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'payments.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'payments.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BarddoUser']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['payments.Payment']", 'unique': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payments.PurchaseStatus']"}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'payments.purchasestatus': {
            'Meta': {'object_name': 'PurchaseStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['payments']