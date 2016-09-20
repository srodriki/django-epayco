import sys

from django.conf import global_settings, settings


settings.configure(

    SECRET_KEY='foobar',
    EPAYCO_TEST_ENV=True,
    EPAYCO_PUBLIC_KEY='45b960805ced5c27ce34b1600b4b9f54',
    EPAYCO_PRIVATE_KEY='5c4773856f296c674685209bbfd11f92',
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    }
)


def runtests(*test_args):
    import django.test.utils

    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

