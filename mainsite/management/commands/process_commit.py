from django.core.management.base import BaseCommand, CommandError

from mainsite.models import Task, Commit, User, Repository


class Command(BaseCommand):
    """
    1 - Save all new tasks with the given commit hash
    2 - Get previous commit from branch, if any
    3 - For each task in the previous commit, check if the task was closed
        or not
        (a task isn't closed if filepath, line_number and text are the same)
    """
    args = 'username repository_name commit_hash branch_name'
    help = ('')

    def handle(self, *args, **options):
        if len(args) != 4:
            raise CommandError('Invalid args')

        username = args[0]
        repository_name = args[1]
        commit_hash = args[2]
        branch_name = args[3]

        repository = self._get_repository(username, repository_name)
        try:
            previous_commit = repository.get_current_commit(branch=branch_name)
        except Commit.DoesNotExist:
            previous_commit = None

        commit = self._process_commit(repository, commit_hash, branch_name)

        if previous_commit is not None:
            self._process_previous_commit(previous_commit, commit)

    def _get_repository(self, username, repository_name):
        user = User.objects.get(username=username)
        return Repository.get_or_create(name=repository_name, user=user)

    def _process_commit(self, repository, commit_hash, branch_name):
        commit = Commit(repository=repository, commit_hash=commit_hash,
                        branch_name=branch_name)
        commit.save()

        dir_extractor = commit._get_dir_extractor()
        for extractor in dir_extractor.get_extractors():
            for extracted_task in extractor.get_tasks():
                task = Task.create_from_extracted_task(extracted_task)
                task.opened_in_commit = commit
                task.save()

        return commit

    def _process_previous_commit(self, previous_commit, current_commit):
        for prev_task in previous_commit.tasks.all():
            cur_task = Task.objects.filter(opened_in_commit=current_commit,
                                           filepath=prev_task.filepath,
                                           line_number=prev_task.line_number,
                                           label=prev_task.label,
                                           username=prev_task.username)
            if not cur_task:
                prev_task.closed_in_commit = current_commit
                prev_task.save()
