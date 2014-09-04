# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'CollectionSubscribeAction'
        db.create_table(u'feed_collectionsubscribeaction', (
            (u'feedaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['feed.FeedAction'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'feed', ['CollectionSubscribeAction'])

        # Adding field 'FeedAction.content_type'
        db.add_column(u'feed_feedaction', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeedAction.object_id'
        db.add_column(u'feed_feedaction', 'object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        if not db.dry_run:
            for action in orm.FeedAction.objects.all():
                action.object_id = action.target.id
                action.save()

        # Deleting field 'FeedAction.target'
        db.delete_column(u'feed_feedaction', 'target_id')


    def backwards(self, orm):
        # Deleting model 'CollectionSubscribeAction'
        db.delete_table(u'feed_collectionsubscribeaction')

        # Adding field 'FeedAction.target'
        db.add_column(u'feed_feedaction', 'target',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.BarddoUser'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'FeedAction.content_type'
        db.delete_column(u'feed_feedaction', 'content_type_id')

        # Deleting field 'FeedAction.object_id'
        db.delete_column(u'feed_feedaction', 'object_id')


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
        u'feed.collectionsubscribeaction': {
            'Meta': {'object_name': 'CollectionSubscribeAction', '_ormbases': [u'feed.FeedAction']},
            u'feedaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.FeedAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.feedaction': {
            'Meta': {'object_name': 'FeedAction'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [],
                                  {'related_name': "u'polymorphic_feed.feedaction_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"})
        },
        u'feed.followaction': {
            'Meta': {'object_name': 'FollowAction', '_ormbases': [u'feed.FeedAction']},
            u'feedaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.FeedAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.joinaction': {
            'Meta': {'object_name': 'JoinAction', '_ormbases': [u'feed.FeedAction']},
            u'feedaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.FeedAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.unfollowaction': {
            'Meta': {'object_name': 'UnFollowAction', '_ormbases': [u'feed.FeedAction']},
            u'feedaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.FeedAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.userfeed': {
            'Meta': {'object_name': 'UserFeed'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.FeedAction']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.BarddoUser']"})
        }
    }

    complete_apps = ['feed']