from django_nose import NoseTestSuiteRunner


class MainSiteNoseTestSuiteRunner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, *args, **kwargs):
        """
        Django nose does not allow us to specify a default app to test, so
        we can subclass to tell django nose to run the specified app if we
        do not specifically provide one on the command line.

        Specifying 'mainsite' causes all submodules of mainsite (i.e. all our
        apps) to be tested, which is what we want.
        """
        if len(test_labels) == 0:
            test_labels = ('codetask', 'mainsite')
        return super(MainSiteNoseTestSuiteRunner, self).run_tests(test_labels,
                                                                  *args,
                                                                  **kwargs)
