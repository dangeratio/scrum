from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):

    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=2000)
    key = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Release(models.Model):

    OPEN, IN_PROGRESS, RESOLVED, CLOSED, NEW = 'Open', 'In Progress', 'Resolved', 'Closed', 'New'
    STATUS_CHOICES = ((NEW, 'New'), (OPEN, 'Open'), (IN_PROGRESS, 'In Progress'), (RESOLVED, 'Resolved'), (CLOSED, 'Closed'), )

    project_id = models.ForeignKey(Project, name='project', db_column='project_id_id', default=0, )
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=2000)
    number = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW, )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


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

    # model fields

    release_id = models.ForeignKey(Release, name='release', db_column='release_id_id', default=0, )
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=2000)
    priority = models.IntegerField(name='priority', db_column='priority', choices=PRIORITY_CHOICES, default=MED, )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Task(models.Model):

    item_id = models.ForeignKey(Item, name='item', db_column='item_id_id', default=0, )
    title = models.CharField(max_length=200)
    detail = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
