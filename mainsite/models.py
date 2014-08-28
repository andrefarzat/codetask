from django.db import models


class Task(models.Model):
    text = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    line_number = models.IntegerField(null=True, default=None)
    opened_in_commit = models.ForeignKey('Commit')
    closed_in_commit = models.ForeignKey('Commit', null=True, default=None)

    @property
    def closed(self):
        return self.closed_in_commit is not None


class Commit(models.Model):
    repository = models.ForeignKey('Repository')
    commit_hash = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)


class Repository(models.Model):
    TYPE_CHOICES = (
        ('local', 'Local'),
        ('github', 'Github'),
        ('bitbucket', 'BitBucket'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,
                            default='local')
