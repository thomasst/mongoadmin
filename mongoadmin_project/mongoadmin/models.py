from django.contrib.auth.models import User
from django.db import models

from pymongo import MongoClient


class MongoConnection(models.Model):
    user = models.ForeignKey(User, null=True)

    name = models.CharField(max_length=255)

    host = models.CharField(max_length=255)
    port = models.IntegerField(default=27017)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    database = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_connection(self):
        #return Connection(self.host, int(self.port), username=self.username, password=self.password)
        # TODO: escaping
        if self.username:
            return MongoClient('mongodb://%s:%s@%s:%d/%s' % (self.username, self.password, self.host, int(self.port), self.database))
        else:
            return MongoClient('mongodb://%s:%d/%s' % (self.host, int(self.port), self.database))
