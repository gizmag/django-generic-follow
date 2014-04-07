# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Follow', fields ['user', 'target_content_type', 'target_object_id']
        db.create_unique(u'generic_follow_follow', ['user_id', 'target_content_type_id', 'target_object_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'Follow', fields ['user', 'target_content_type', 'target_object_id']
        db.delete_unique(u'generic_follow_follow', ['user_id', 'target_content_type_id', 'target_object_id'])

    models = {
        "%s.%s" % (User._meta.app_label, User._meta.module_name): {
            'Meta': {'object_name': User.__name__},
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic_follow.follow': {
            'Meta': {'unique_together': "(('user', 'target_content_type', 'target_object_id'),)", 'object_name': 'Follow'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'following'", 'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
    }

    complete_apps = ['generic_follow']
