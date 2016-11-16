# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'StringHolder.absolute_url'
        db.alter_column(u'django_bitly_stringholder', 'absolute_url', self.gf('django.db.models.fields.URLField')(max_length=1024))

    def backwards(self, orm):

        # Changing field 'StringHolder.absolute_url'
        db.alter_column(u'django_bitly_stringholder', 'absolute_url', self.gf('django.db.models.fields.URLField')(max_length=200))

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
            'absolute_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_bitly']