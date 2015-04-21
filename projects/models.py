from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):

    class Meta:
        db_table = 'projects'

    # user_list = User.objects.filter(active=1)

    title = models.CharField(max_length=200)
    detail = models.TextField()
    key_title = models.CharField(max_length=5)
    owner = models.ForeignKey(User, db_column='username')













