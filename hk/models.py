import datetime, urlparse
from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)
    about = models.TextField(blank = True)
    email = models.EmailField()
    register_date = models.DateTimeField(default = datetime.datetime.now())


class Item(models.Model):
    ITEM_TYPE_CHOICES = (
            ('NEW', 'New'),
            ('COMMENT', 'Comment'),
        )

    type = models.CharField(max_length = 20, choices = ITEM_TYPE_CHOICES, default = 'NEW')
    title = models.CharField(max_length = 100)
    url = models.URLField(blank = True)
    text = models.TextField(blank = True)
    parent = models.ForeignKey('self', null = True, blank = True)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField(default = datetime.datetime.now())
    points = models.IntegerField(default = 0)
    scores = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)

    def formated_create_time(self):
        now = timezone.now() # offset-awared datetime
        now.astimezone(timezone.utc).replace(tzinfo = None) # change to offset-native datetime
        delta = now - self.create_date
        if delta.days > 0:
            return "%s day(s) ago" % (delta.days)
        else:
            if (delta.seconds / 3600) > 0:
                return "%s hour(s) ago" % (delta.seconds / 3600)
            else:
                return "%s minute(s) ago" % (delta.seconds / 60)

    def get_domain(self):
        return urlparse.urlsplit(self.url).netloc if self.url else ''

class Point(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)

