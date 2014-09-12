# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Notification'
        db.create_table(u'notifications_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_notifications.notification_set', null=True,
                                                                                        to=orm['contenttypes.ContentType'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['accounts.BarddoUser'])),
            ('unread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('actor_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_actor', to=orm['contenttypes.ContentType'])),
            ('actor_object_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('target_content_type',
             self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='notify_target', null=True, to=orm['contenttypes.ContentType'])),
            ('target_object_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('action_object_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='notify_action_object', null=True,
                                                                                                 to=orm['contenttypes.ContentType'])),
            ('action_object_object_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'notifications', ['Notification'])

        # Adding model 'WorkPublishedNotification'
        db.create_table(u'notifications_workpublishednotification',
                        ((u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Notification'],
                                                                                                        unique=True, primary_key=True)),))
        db.send_create_signal(u'notifications', ['WorkPublishedNotification'])

        # Adding model 'WorkLikedNotification'
        db.create_table(u'notifications_worklikednotification', (
            (
                u'notification_ptr',
                self.gf('django.db.models.fields.related.OneToOneField')(to=orm['notifications.Notification'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'notifications', ['WorkLikedNotification'])

    def backwards(self, orm):
        # Deleting model 'Notification'
        db.delete_table(u'notifications_notification')

        # Deleting model 'WorkPublishedNotification'
        db.delete_table(u'notifications_workpublishednotification')

        # Deleting model 'WorkLikedNotification'
        db.delete_table(u'notifications_worklikednotification')


    models = {
        u'accounts.barddouser': {
            'Meta': {'object_name': 'BarddoUser', 'index_together': "[['username', 'first_name', 'last_name']]"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_publisher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)",
                     'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType',
                     'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notifications.notification': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Notification'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [],
                                           {'blank': 'True', 'related_name': "'notify_action_object'", 'null': 'True',
                                            'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [],
                                  {'related_name': "u'polymorphic_notifications.notification_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': u"orm['accounts.BarddoUser']"}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [],
                                    {'blank': 'True', 'related_name': "'notify_target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'notifications.worklikednotification': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'WorkLikedNotification', '_ormbases': [u'notifications.Notification']},
            u'notification_ptr': (
                'django.db.models.fields.related.OneToOneField', [], {'to': u"orm['notifications.Notification']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'notifications.workpublishednotification': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'WorkPublishedNotification', '_ormbases': [u'notifications.Notification']},
            u'notification_ptr': (
                'django.db.models.fields.related.OneToOneField', [], {'to': u"orm['notifications.Notification']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['notifications']