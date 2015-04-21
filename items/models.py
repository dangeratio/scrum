from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    class Meta:
        db_table = 'items'

    # define static values

    BUG, IMPROVEMENT, FEATURE, TASK = 'b', 'i', 'f', 't'

    TYPE_CHOICES = (
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Improvement'),
        (FEATURE, 'Feature'),
        (TASK, 'Task'),
    )

    LOW, LOW_MED, MED, MED_HIGH, HIGH = 1, 2, 3, 4, 5

    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (LOW_MED, 'Low-Med'),
        (MED, 'Medium'),
        (MED_HIGH, 'Medium-High'),
        (HIGH, 'High'),
    )

    HOUR, HOURS, DAY, DAYS, WEEK, WEEKS = 1, 2, 3, 4, 5, 6

    EFFORT_CHOICES = (
        (HOUR, 'Hour'),
        (HOURS, 'Hours'),
        (DAY, 'Day'),
        (DAYS, 'Days'),
        (WEEK, 'Week'),
        (WEEKS, 'Weeks'),
    )

    key = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    detail = models.TextField()
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES,
                            default=BUG)
    priority = models.IntegerField(choices=PRIORITY_CHOICES,
                                   default=MED)
    effort = models.IntegerField(choices=EFFORT_CHOICES,
                                 default=DAY)
    # sprint = models.ForeignKey(Release, db_column='title')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_started = models.DateTimeField()
    date_completed = models.DateTimeField()
    owner = models.ForeignKey(User, db_column='username')
    # submitter = models.ForeignKey(User, db_column='username')
