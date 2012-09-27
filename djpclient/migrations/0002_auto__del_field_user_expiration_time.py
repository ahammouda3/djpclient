# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.expiration_time'
        db.delete_column('djpclient_user', 'expiration_time')


    def backwards(self, orm):
        # Adding field 'User.expiration_time'
        db.add_column('djpclient_user', 'expiration_time',
                      self.gf('django.db.models.fields.DecimalField')(default=datetime.datetime(2012, 9, 27, 0, 0), max_digits=20, decimal_places=10),
                      keep_default=False)


    models = {
        'djpclient.user': {
            'Meta': {'object_name': 'User'},
            'analytics_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 27, 0, 0)'})
        }
    }

    complete_apps = ['djpclient']