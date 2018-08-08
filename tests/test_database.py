class TestCRUD:
    def test_add_one(self, db):
        result = db.add_one(
            {'name': 'alice', 'url': 'alice.com', 'method': 'get'})

        errors = result.get('errors')
        success = result.get('success')

        assert errors is None
        assert success is True

    def test_fetch_one(self, db, db_dummy_data):
        result = db.fetch_one(name='alice')

        assert result.name == 'alice'
        assert result.url == 'alice.com'
        assert result.method == 'get'

    def test_update_one(self, db, db_dummy_data):
        result = db.fetch_one(name='alice')

        db.update_one(rowid=result.rowid, values={
            'name': 'eve', 'method': 'post', 'url': 'example.com'})

        result = db.fetch_one(name='eve')

        assert result.name == 'eve'
        assert result.method == 'post'

    def test_fetch_all(self, db, db_dummy_data):
        rows = db.fetch_all()

        assert len(rows) == 2

    def test_delete_one(self, db, db_dummy_data):
        before_delete = db.fetch_all()

        db.delete_one(name='alice')

        after_delete = db.fetch_all()

        assert len(before_delete) == len(after_delete) + 1


class TestErrors:

    def test_add_one_missing_column(self, db):
        result = db.add_one({})

        errors = result.get('errors')

        assert errors == 'missing column error: name'

        result = db.add_one(
            {'name': 'alice'})

        errors = result.get('errors')

        assert errors == 'missing column error: url'

        result = db.add_one(
            {'name': 'alice', 'url': 'alice.com'})

        errors = result.get('errors')

        assert errors == 'missing column error: method'

        result = db.add_one(
            {'name': 'alice', 'url': 'alice.com', 'method': 'get'})

        errors = result.get('errors')

        assert errors is None

    def test_constraint_violation(self, db, db_dummy_data):
        result = db.add_one(
            {'name': 'alice', 'url': 'alice.com', 'method': 'get'})

        errors = result.get('errors')

        assert errors == '{}'.format(
            'sqlite error: UNIQUE constraint failed: requests.name')


class TestSort:

    def test_sort(self, db, db_dummy_data):

        name_asc = db.fetch_all(sort_by='name', order='asc')
        assert name_asc[0].name == 'alice'
        assert name_asc[1].name == 'bob'

        name_desc = db.fetch_all(sort_by='name', order='desc')
        assert name_desc[0].name == 'bob'
        assert name_desc[1].name == 'alice'

        time_asc = db.fetch_all(sort_by='timestamp', order='asc')
        assert time_asc[0].name == 'alice'
        assert time_asc[1].name == 'bob'

        time_desc = db.fetch_all(sort_by='timestamp', order='desc')
        assert time_desc[0].name == 'bob'
        assert time_desc[1].name == 'alice'

