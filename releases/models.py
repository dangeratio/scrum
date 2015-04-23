from django.db import models
from projects.models import Project


class Release(models.Model):

    class Meta:
        db_table = 'releases'

    # define static values

    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    CLOSED = 'Closed'
    NEW = 'New'

    STATUSES = (OPEN, IN_PROGRESS, RESOLVED, CLOSED, NEW)

    STATUS_CHOICES = (
        (NEW, 'New'),
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
        (CLOSED, 'Closed'),
    )

    number = models.FloatField(default='')
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=OPEN,)
    detail = models.TextField(default='')
    start_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(default='')
    project_id = models.ForeignKey(Project)

    total_items = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title