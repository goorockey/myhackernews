import datetime, urlparse
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Hacker(AbstractUser):
    about = models.TextField(blank = True)


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
    scores = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)

    def set_comments(self, comments):
        self.comments = comments
        self.calc_score()

    def set_points(self, points):
        self.points = points
        self.calc_score()


    def calc_score(self):
        delta = self.get_past_time()
        self.scores = (self.points + self.comments) / ((self.seconds / 3600 + 1) ** GRAVITY) 
        

    def get_past_time(self):
        now = timezone.now() # offset-awared datetime
        now.astimezone(timezone.utc).replace(tzinfo = None) # change to offset-native datetime
        delta = now - self.create_date
        return delta

    def formated_create_time(self):
        delta = self.get_past_time()
        if delta.days > 0:
            return "%s day(s) ago" % (delta.days)
        else:
            if (delta.seconds / 3600) > 0:
                return "%s hour(s) ago" % (delta.seconds / 3600)
            else:
                return "%s minute(s) ago" % (delta.seconds / 60)

    def get_domain(self):
        return urlparse.urlsplit(self.url).netloc if self.url else ''

    def childs(self):
        return Item.objects.filter(parent_id = self.id)

class Point(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)

