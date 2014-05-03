# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table(u'feedback_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('feedback', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'feedback', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table(u'feedback_feedback')


    models = {
        u'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['feedback']