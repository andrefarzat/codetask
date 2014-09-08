from django.views.generic import FormView
from django import forms

from codetask.extractor import DirExtractor
from mainsite.models import Task, Commit, Repository


class HomeForm(forms.Form):
    repository = forms.CharField(label='Repository', max_length=100)


class HomePageView(FormView):
    template_name = 'mainsite/home.html'
    form_class = HomeForm
    success_url = '/'

    # todo: remove later
    commit = 'e2fc714c4727ee9395f324cd2e7f331f'

    def form_valid(self, form):
        self.do_extraction(form.cleaned_data['repository'])
        return super(HomePageView, self).form_valid(form)

    def do_extraction(self, repository_path):
        dir_extractor = DirExtractor(repository_path)

        for extractor in dir_extractor.get_extractors():
            for task in extractor.get_tasks():
                if task.is_valid():
                    self.add_task(task)

    def add_task(self, extracted_task):
        task = Task.create_from_extracted_task(extracted_task)
        task.opened_in_commit = self._get_commit()
        task.save()

    def _get_commit(self):
        if getattr(self, '_commit', None) is None:
            repository = Repository(owner=self.request.user)
            self._commit = Commit.objects.get_or_create(repository=repository,
                                                        name='initial_test',
                                                        type='local')
        return self._commit
