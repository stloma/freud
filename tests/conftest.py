import pytest
import json
import os
import sys


def pytest_configure():
    """ Freud checks for this upon startup. If true, creates a new test.db """

    sys._called_from_test = True


def pytest_unconfigure():
    from freud import DB_FILE
    from freud.model import basedir

    del sys._called_from_test
    os.remove(os.path.join(basedir, DB_FILE))


@pytest.fixture(scope='class')
def db_conn():

    from freud.model import Db
    db = Db()

    yield db


@pytest.fixture(scope='function')
def db(db_conn):

    db_conn.delete_all()

    return db_conn


@pytest.fixture(scope='function')
def db_dummy_data(db):
    db.add_one(
        {'name': 'alice', 'url': 'alice.com', 'method': 'get'})

    db.add_one(
        {'name': 'bob', 'url': 'bob.com', 'method': 'get'})

    return


@pytest.fixture(scope='class')
def db_request_data(httpbin, db_conn):

    # Get request
    #
    db_conn.add_one({
        'name': 'httpbin-get',
        'url': '{}/get'.format(httpbin.url),
        'method': 'GET'
    })

    # Delete request
    #
    db_conn.add_one({
        'name': 'httpbin-delete',
        'url': '{}/delete'.format(httpbin.url),
        'method': 'DELETE',
    })

    # Patch request
    #
    db_conn.add_one({
        'name': 'httpbin-patch',
        'url': '{}/patch'.format(httpbin.url),
        'method': 'PATCH',
    })

    # Put request
    #
    db_conn.add_one({
        'name': 'httpbin-put',
        'url': '{}/put'.format(httpbin.url),
        'method': 'PUT',
    })

    # Post request
    #
    db_conn.add_one({
        'name': 'httpbin-post',
        'url': '{}/post'.format(httpbin.url),
        'method': 'POST',
        'body': json.dumps({'name': 'alice'}),
        'headers': json.dumps({'Content-Type': 'application/json'})
    })

    # Post form
    #
    db_conn.add_one({
        'name': 'httpbin-post-form',
        'url': '{}/post'.format(httpbin.url),
        'method': 'POST',
        'headers': json.dumps(
            {'content-type': 'application/x-www-form-urlencoded'}
        ),
        'body': 'name=alice&email=alice@email.com'
    })

    # Basic auth
    #
    db_conn.add_one({
        'name': 'httpbin-basic-auth-200',
        'url': '{}/basic-auth/alice/password'.format(httpbin.url),
        'method': 'GET',
        'auth': json.dumps({
            'user': 'alice',
            'password': 'password',
            'type': 'basic'
        })
    })
    db_conn.add_one({
        'name': 'httpbin-basic-auth-401',
        'url': '{}/basic-auth/alice/password'.format(httpbin.url),
        'method': 'GET',
        'auth': json.dumps({
            'user': 'eve',
            'password': 'bad_password',
            'type': 'basic'
        })
    })
    db_conn.add_one({
        'name': 'httpbin-digest-auth-200',
        'url': '{}/digest-auth/auth/alice/password'.format(httpbin.url),
        'method': 'GET',
        'auth': json.dumps({
            'user': 'alice',
            'password': 'password',
            'type': 'digest'
        })
    })
    db_conn.add_one({
        'name': 'httpbin-digest-auth-401',
        'url': '{}/digest-auth/auth/alice/password'.format(httpbin.url),
        'method': 'GET',
        'auth': json.dumps({
            'user': 'eve',
            'password': 'bad_password',
            'type': 'digest'
        })
    })

    return
