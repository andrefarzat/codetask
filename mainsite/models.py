import os

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from codetask.extractor import DirExtractor


class User(AbstractUser):
    pass


class Repository(models.Model):
    TYPE_CHOICES = (
        ('local', 'Local'),
        ('github', 'Github'),
        ('bitbucket', 'BitBucket'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,
                            default='local')

    def get_current_commit(self, branch_name='master'):
        try:
            return self.commits.filter(branch_name=branch_name)[0]
        except IndexError:
            raise self.DoesNotExist()

    def get_path(self):
        """Returns the file system path to repository dir"""
        return os.path.join(settings.BASE_DIR, '')


class Task(models.Model):
    text = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    line_number = models.IntegerField(null=True, default=None)
    label = models.CharField(max_length=255, null=True, default=None)
    username = models.CharField(max_length=255, null=True, default=None)
    opened_in_commit = models.ForeignKey('Commit', related_name='opened_tasks')
    closed_in_commit = models.ForeignKey('Commit', null=True, default=None,
                                         related_name='closed_tasks')

    @property
    def closed(self):
        return self.closed_in_commit is not None

    @property
    def commit(self):
        return self.opened_in_commit

    @property
    def filename(self):
        return os.path.split(self.filepath)[1]

    @classmethod
    def create_from_extracted_task(cls, extracted_task):
        task = cls()
        task.text = extracted_task.text
        task.filepath = extracted_task.filepath
        task.line_number = extracted_task.line_number
        task.label = extracted_task.label
        task.username = extracted_task.username
        return task


class Commit(models.Model):
    repository = models.ForeignKey('Repository', related_name='commits')
    commit_hash = models.CharField(max_length=255)
    commit_time = models.DateTimeField(auto_now_add=True)
    branch_name = models.CharField(max_length=255)

    def get_dir_extractor(self):
        path = self.repository.get_path()
        return DirExtractor(path)
