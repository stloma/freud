import sqlite3
import os
import datetime
from collections import namedtuple

from freud import DB_FILE, SORT_BY

basedir = 'config/'


class Db:

    def __init__(self, database=DB_FILE):

        self.database = database
        self.connect()
        self.close()

    def namedtuple_factory(self, cursor, row):
        """ Returns namedtuple results, named with column names """

        fields = [col[0] for col in cursor.description]
        Row = namedtuple('Row', fields)
        return Row(*row)

    def connect(self):

        self.conn = sqlite3.connect(
            os.path.join(basedir, self.database),
            detect_types=sqlite3.PARSE_COLNAMES
        )
        self.conn.row_factory = self.namedtuple_factory
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                            name text not null unique,
                            timestamp timestamp,
                            url text not null,
                            method text not null,
                            body text,
                            auth text,
                            headers text
                            )
                    ''')

    def close(self):

        self.conn.commit()
        self.conn.close()

    def fetch_all(self, sort_by=None, order=None):
        """ Returns all rows """

        sort_by = sort_by if sort_by else SORT_BY['column']
        order = order if order else SORT_BY['order']

        self.connect()

        if sort_by and order:
            self.cursor.execute(
                'SELECT * FROM requests ORDER BY {} {}'.format(sort_by, order))
        elif sort_by:
            self.cursor.execute(
                'SELECT * FROM requests ORDER BY {sort_by}'.format(sort_by))
        else:
            self.cursor.execute('SELECT * FROM requests')

        rows = self.cursor.fetchall()

        self.close()

        return rows

    def fetch_one(self, rowid=None, name=None):

        self.connect()

        if rowid:
            self.cursor.execute('''SELECT * FROM requests WHERE rowid = ?''',
                                (rowid,))
        else:
            self.cursor.execute('''
                    SELECT rowid, * FROM requests WHERE name = ?''',
                                (name,))

        result = self.cursor.fetchone()

        if result:
            return result

        return False

        self.close()

    def add_one(self, values):

        self.connect()

        try:
            with self.conn:
                self.conn.execute('''INSERT INTO requests
                                 (
                                  name, url, method, timestamp, auth,
                                  body, headers)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                  (
                                      values['name'],
                                      values['url'],
                                      values['method'],
                                      datetime.datetime.now(),
                                      values.get('auth'),
                                      values.get('body'),
                                      values.get('headers')
                                  ))
        except sqlite3.IntegrityError as e:
            return {'errors': 'sqlite error: {}'.format(e.args[0])}

        except KeyError as e:
            return {'errors': 'missing column error: {}'.format(e.args[0])}

        finally:
            self.close()

        return {'success': True}

    def delete_one(self, name):

        self.connect()
        self.cursor.execute('''DELETE FROM requests WHERE name = ?''',
                            (name,))

        self.close()

    def delete_all(self):
        """ Used for testing """

        self.connect()
        self.cursor.execute('''DELETE FROM requests''')

        self.close()

    def update_one(self, values=None, rowid=None):
        """ Updates one row by rowid if supplied, else by name """

        self.connect()

        if rowid:
            # If the rowid is set, we could be changing the name
            name = values.get('name')
            url = values.get('url')
            method = values.get('method')

            if not all([name, url, method]):
                return {'errors': 'Name, url, and method are required'}

            try:
                with self.conn:
                    self.conn.execute('''UPDATE requests SET
                            url=?, method=?, name=? where rowid=?''',
                                      (url, method, name, rowid))

            except sqlite3.IntegrityError as e:
                return {'errors': 'sqlite error: {}'.format(e.args[0])}

            except KeyError as e:
                return {
                    'errors':  'missing column error: {}'.format(e.args[0])}

            finally:
                self.close()

        else:
            # Changes all fields passed in through values
            name = values.get('name')

            result = self.fetch_one(name=name)

            body = values.get('body', result.body)
            headers = values.get('headers', result.headers)
            auth = values.get('auth', result.auth)

            self.connect()

            try:

                with self.conn:
                    self.conn.execute('''
                            UPDATE requests SET
                            body=?, headers=?, auth=?
                            where name=?''',
                                      (body, headers, auth,
                                       name
                                       )
                                      )

            except sqlite3.IntegrityError as e:
                return {'errors': 'sqlite error: {}'.format(e.args[0])}

            except KeyError as e:
                return {'errors': 'missing column error: {}'.format(e.args[0])}

            finally:
                self.close()

        return {'success': True}


db = Db()
