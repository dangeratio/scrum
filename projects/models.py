from django.db import models
from django.contrib.auth.models import User


# this model is used to store details about each project
#
class Project(models.Model):

    title = models.CharField(max_length=200, )
    detail = models.TextField(max_length=2000, )
    key = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


# this model is used to store the various details about each release within a project
#
class Release(models.Model):

    OPEN, IN_PROGRESS, RESOLVED, CLOSED, NEW = 'Open', 'In Progress', 'Resolved', 'Closed', 'New'
    STATUS_CHOICES = ((NEW, 'New'), (OPEN, 'Open'), (IN_PROGRESS, 'In Progress'), (RESOLVED, 'Resolved'), (CLOSED, 'Closed'), )

    project_id = models.ForeignKey(Project, name='project', db_column='project_id_id', default=0, )
    title = models.CharField(max_length=200, )
    detail = models.TextField(max_length=2000, )
    number = models.FloatField(default=0.0, )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW, )
    # is_backlog = models.BooleanField(default=False, )

    date_created = models.DateTimeField(name='date_created', db_column='date_created', auto_now_add=True, )
    date_modified = models.DateTimeField(name='date_modified', db_column='date_modified', auto_now=True, )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


# this model is used to store work items within each release
#
class Item(models.Model):

    # static items

    LOW, MED_LOW, MED, MED_HIGH, HIGH = 1, 2, 3, 4, 5

    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MED_LOW, 'Medium-Low'),
        (MED, 'Medium'),
        (MED_HIGH, 'Medium-High'),
        (HIGH, 'High'),
    )

    NEW, OPEN, IN_PROGRESS, CLOSED_ACTION, CLOSED_NO_ACTION = 1, 2, 3, 4, 5

    STATUS_CHOICES = (
        (NEW, 'New'),
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSED_ACTION, 'Closed-Action'),
        (CLOSED_NO_ACTION, 'Closed-No Action'),
    )

    # model fields

    release_id = models.ForeignKey(Release, name='release', db_column='release_id_id', default=0, )
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=2000, )
    priority = models.IntegerField(name='priority', db_column='priority', choices=PRIORITY_CHOICES, default=MED, )
    status = models.IntegerField(name='status', db_column='status', choices=STATUS_CHOICES, default=NEW, )

    date_created = models.DateTimeField(name='date_created', db_column='date_created', auto_now_add=True, )
    date_modified = models.DateTimeField(name='date_modified', db_column='date_modified', auto_now=True, )
    date_started = models.DateTimeField(name='date_started', db_column='date_started', blank=True, null=True, )
    date_completed = models.DateTimeField(name='date_completed', db_column='date_completed', blank=True, null=True, )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


# this model is used for storing individual tasks associated with each item
#
class Task(models.Model):

    item_id = models.ForeignKey(Item, name='item', db_column='item_id_id', default=0, )
    title = models.CharField(max_length=200, )
    detail = models.TextField(max_length=2000, )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


# this model is used to store report data for the project burn down chart
#
class ItemLog(models.Model):

    project_id = models.ForeignKey(Project, name='project', db_column='project_id_id', default=0, )
    day = models.DateField()
    total_open = models.IntegerField()
    total_closed = models.IntegerField()


# this model is used to store a history log of comments on an item
#
class ItemComments(models.Model):

    item_id = models.ForeignKey(Item, name='item', db_column='item_id', default=0, )
    date_created = models.DateTimeField(name='date_created', db_column='date_created', auto_now_add=True, )
    comment = models.TextField(max_length=2000, )



