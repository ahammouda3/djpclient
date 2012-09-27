from django.db import models

from datetime import datetime

class User(models.Model):
    '''                                                                                                                                                                           
    This table is meant soley to create reliable and fast unique id's for each user                                                                                               
    to be used in sessions                                                                                                                                                        
                                                                                                                                                                                  
    The other fields besides analytics_id may choose to be useful for speed as well.                                                                                              
    '''
    analytics_id = models.AutoField(primary_key=True)
    creation_time = models.DateTimeField(null=False, default=datetime.now())
    "make it a time delta to prevent end of month failure"
    "This field is the result of calling total_seconds() on a timedelta"
    expiration_time = models.DateTimeField(null=False,blank=False)
    #expiration_time = models.DecimalField(null=False, max_digits=20, decimal_places=10)
