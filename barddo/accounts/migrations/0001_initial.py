# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from MySQLdb.cursors import Warning


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):
        # Adding model 'BarddoUser'
        db.create_table(u'accounts_barddouser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'accounts', ['BarddoUser'])

        # Detect if application supports fulltext search on given backend
        if not db.dry_run and db.backend_name == "mysql":
            try:
                db.execute("CREATE FULLTEXT INDEX fix_accounts_barddouser ON accounts_barddouser (username, first_name, last_name)")
            except Warning:
                pass
        else:
            # Adding index on 'BarddoUser', fields ['username', 'first_name', 'last_name']
            db.create_index(u'accounts_barddouser', ['username', 'first_name', 'last_name'])

        # Adding M2M table for field groups on 'BarddoUser'
        m2m_table_name = db.shorten_name(u'accounts_barddouser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('barddouser', models.ForeignKey(orm[u'accounts.barddouser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['barddouser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'BarddoUser'
        m2m_table_name = db.shorten_name(u'accounts_barddouser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('barddouser', models.ForeignKey(orm[u'accounts.barddouser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['barddouser_id', 'permission_id'])

        # Adding model 'BarddoUserProfile'
        db.create_table(u'accounts_barddouserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True,
                                                                              to=orm['accounts.BarddoUser'])),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 5, 3, 0, 0))),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('country', self.gf('django.db.models.fields.CharField')(default=u'Brazil', max_length='30')),
        ))
        db.send_create_signal(u'accounts', ['BarddoUserProfile'])


    def backwards(self, orm):
        # Removing index on 'BarddoUser', fields ['username', 'first_name', 'last_name']
        db.delete_index(u'accounts_barddouser', ['username', 'first_name', 'last_name'])

        # Deleting model 'BarddoUser'
        db.delete_table(u'accounts_barddouser')

        # Removing M2M table for field groups on 'BarddoUser'
        db.delete_table(db.shorten_name(u'accounts_barddouser_groups'))

        # Removing M2M table for field user_permissions on 'BarddoUser'
        db.delete_table(db.shorten_name(u'accounts_barddouser_user_permissions'))

        # Deleting model 'BarddoUserProfile'
        db.delete_table(u'accounts_barddouserprofile')


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
        u'accounts.barddouserprofile': {
            'Meta': {'object_name': 'BarddoUserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 3, 0, 0)'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'Brazil'", 'max_length': "'30'"}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [],
                     {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['accounts.BarddoUser']"})
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
        }
    }

    complete_apps = ['accounts']