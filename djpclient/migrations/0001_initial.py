# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('djpclient_user', (
            ('analytics_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 27, 0, 0))),
            ('expiration_time', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=10)),
        ))
        db.send_create_signal('djpclient', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('djpclient_user')


    models = {
        'djpclient.user': {
            'Meta': {'object_name': 'User'},
            'analytics_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 27, 0, 0)'}),
            'expiration_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '10'})
        }
    }

    complete_apps = ['djpclient']