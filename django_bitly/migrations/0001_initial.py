# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StringHolder'
        db.create_table(u'django_bitly_stringholder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('absolute_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'django_bitly', ['StringHolder'])

        # Adding model 'Bittle'
        db.create_table(u'django_bitly_bittle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('absolute_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('shortKeywordUrl', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('shortUrl', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('userHash', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('statstring', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('statstamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'django_bitly', ['Bittle'])


    def backwards(self, orm):
        # Deleting model 'StringHolder'
        db.delete_table(u'django_bitly_stringholder')

        # Deleting model 'Bittle'
        db.delete_table(u'django_bitly_bittle')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_bitly.bittle': {
            'Meta': {'ordering': "('-date_created',)", 'object_name': 'Bittle'},
            'absolute_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shortKeywordUrl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'shortUrl': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'statstamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'statstring': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'userHash': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'django_bitly.stringholder': {
            'Meta': {'object_name': 'StringHolder'},
            'absolute_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_bitly']