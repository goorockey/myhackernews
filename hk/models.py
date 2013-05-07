import datetime, urlparse
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def get_past_time(dt):
    now = timezone.now() # offset-awared datetime
    now.astimezone(timezone.utc).replace(tzinfo = None) # change to offset-native datetime
    delta = now - dt
    return delta

def formated_past_time(delta):
    if delta.days > 0:
        return "%s day(s) ago" % (delta.days)
    else:
        if (delta.seconds / 3600) > 0:
            return "%s hour(s) ago" % (delta.seconds / 3600)
        else:
            return "%s minute(s) ago" % (delta.seconds / 60)


class Hacker(AbstractUser):
    about = models.TextField(blank = True)

    def formated_create_time(self):
        return formated_past_time(get_past_time(self.date_joined))


class Item(models.Model):
    GRAVITY = 1.8
    ITEM_TYPE_CHOICES = (
            ('NEW', 'New'),
            ('COMMENT', 'Comment'),
        )

    type = models.CharField(max_length = 20, choices = ITEM_TYPE_CHOICES, default = 'NEW')
    title = models.CharField(max_length = 100, blank = True)
    url = models.URLField(blank = True)
    text = models.TextField(blank = True)
    parent = models.ForeignKey('self', null = True, blank = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_date = models.DateTimeField(default = datetime.datetime.now())
    points = models.IntegerField(default = 0)
    score = models.FloatField(default = 0)
    comments = models.IntegerField(default = 0)

    def comments_inc(self):
        item = self
        while item:
            item.comments = item.comments + 1
            item.calc_score()
            item.save()

            item = item.parent

    def points_inc(self):
        self.points = self.points + 1
        self.calc_score()
        self.save()

    def calc_score(self):
        delta = self.get_past_time()
        self.score = float(self.points + self.comments) / ((delta.seconds / 3600 + 1) ** self.GRAVITY) 

    def get_past_time(self):
        return get_past_time(self.create_date)

    def formated_create_time(self):
        return formated_past_time(self.get_past_time())

    def get_domain(self):
        return urlparse.urlsplit(self.url).netloc if self.url else ''

    def childs(self):
        return Item.objects.filter(parent_id = self.id)
