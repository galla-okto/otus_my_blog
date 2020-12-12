from pytest import fixture


@fixture(scope='class')
def user():
    return 1
