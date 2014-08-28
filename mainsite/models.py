from django.db import models


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


class Commit(models.Model):
    repository = models.ForeignKey('Repository')
    commit_hash = models.CharField(max_length=255)
    commit_time = models.DateTimeField(auto_now_add=True)
    branch_name = models.CharField(max_length=255)


class Repository(models.Model):
    TYPE_CHOICES = (
        ('local', 'Local'),
        ('github', 'Github'),
        ('bitbucket', 'BitBucket'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,
                            default='local')
