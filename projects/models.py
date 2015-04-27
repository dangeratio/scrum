from django.db import models


class Project(models.Model):

    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=2000)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Release(models.Model):

    project_id = models.ForeignKey(Project, name='project', db_column='project_id_id')
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=2000)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Item(models.Model):

    release_id = models.ForeignKey(Release, name='release', db_column='release_id_id')
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=2000)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Task(models.Model):

    item_id = models.ForeignKey(Item, name='item', db_column='item_id_id')
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=2000)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
