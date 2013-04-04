from django.db import models
import datetime

class User(models.Model):
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)
    about = models.TextField(blank = True)
    email = models.CharField(max_length = 50)
    register_date = models.DateTimeField(default = datetime.datetime.now())

class New(models.Model):
    title = models.CharField(max_length = 100)
    url = models.TextField(null = True)
    text = models.TextField(null = True)
    author_id = models.ForeignKey(User)
    create_date = models.DateTimeField(default = datetime.datetime.now())
    points = models.IntegerField(default = 0)
    scores = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)

class Comment(models.Model):
    author_id = models.ForeignKey(User)
    parent_id = models.ForeignKey('self')
    create_date = models.DateTimeField(default = datetime.datetime.now())
    points = models.IntegerField(default = 0)
    scores = models.IntegerField(default = 0)
    comments = models.IntegerField(default = 0)

class New_Points(models.Model):
    user_id = models.ForeignKey(User)
    new_id = models.ForeignKey(New)

class Comment_Points(models.Model):
    user_id = models.ForeignKey(User)
    comment_id = models.ForeignKey(Comment)
    
