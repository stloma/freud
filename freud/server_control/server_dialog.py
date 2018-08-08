from prompt_toolkit.layout.dimension import D
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Dialog, Label, Button
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout import Float

from freud.ui.root_container import root_container
from freud.model import db
from freud.utils import ButtonManager, select_item
from freud.ui.dialog import ErrorDialog


class ServerDialog:
    def __init__(self, event, create_server=False):

        def ok_handler():

            # Simplistic check to see if user forgot to enter something for url
            url = len(self.url.text) > len('https://')

            if not all([self.name.text, url, self.method.text]):
                return ErrorDialog(event, title='Input Error',
                                   text='Name, Url, and Method are required.')

            result = server_to_db()

            if result.get('success'):

                root_container.floats.pop()

                # Rather than inserting a new button into, e.g.,
                # hsplit.children, we recreate the layout since we have to
                # pay attention to sort order here
                event.app.layout = Layout(root_container.create())

                # Find the button in the redrawn layout; then focus on it
                buttons = ButtonManager.update_buttons(event.app)
                for button in buttons:
                    if self.name.text == button.content.text()[1][1].strip():
                        event.app.layout.focus(button)
                        break

                select_item(event)

            else:
                # Add/update server returned an error
                ErrorDialog(event, title='Add/edit server error',
                            text=str(result.get('errors')))

        def cancel_handler():
            root_container.floats.pop()
            if ButtonManager.prev_button:
                event.app.layout.focus(ButtonManager.prev_button)

        def server_to_db():
            if self.rowid:
                # Updating an existing server
                return db.update_one(
                    rowid=self.rowid,
                    values={
                        'name': self.name.text,
                        'url': self.url.text,
                        'method': self.method.text
                    })
            else:
                # Creating a new server
                return db.add_one(
                    values={
                        'name': self.name.text,
                        'url': self.url.text,
                        'method': self.method.text
                    })

        # Get data about server currently editing
        if create_server:
            title = 'New Server'
            self.rowid = None
            name = ''
            url = 'https://'
            method = ''
        else:
            title = 'Edit Server'
            self.name = ButtonManager.current_button
            result = db.fetch_one(name=self.name)

            self.rowid = result.rowid
            name = result.name
            url = result.url
            method = result.method

        # Dialog configuration
        ok_button = Button(text='OK', handler=ok_handler)
        cancel_button = Button(text='Cancel', handler=cancel_handler)

        methods = [
            'GET',
            'POST',
            'PUT',
            'HEAD',
            'DELETE',
            'CONNECT',
            'OPTIONS',
            'TRACE',
            'PATCH'
        ]
        method_completer = WordCompleter(methods,
                                         ignore_case=True)

        local_kb = KeyBindings()

        @local_kb.add('enter')
        def cancel_completion(event):
            buff = event.app.current_buffer
            buff.complete_state = None
            event.app.layout.focus_next()

        self.name = TextArea(
            multiline=False,
            text=name
        )
        self.name.buffer.document = Document(name, len(name))

        self.url = TextArea(
            multiline=False,
            text=url
        )
        self.url.buffer.document = Document(url, len(url))

        self.method = TextArea(
            multiline=False,
            completer=method_completer,
            text=method)
        self.method.buffer.document = Document(method, len(method))

        self.dialog = Dialog(
            title=title,
            body=HSplit([
                Label(text='Server name:\n'),
                self.name,
                Window(height=1, char=' '),
                Label(text='Url:\n'),
                self.url,
                Window(height=1, char=' '),
                Label(text='Method:\n'),
                self.method,
                Window(height=1, char=' ')
            ],
                key_bindings=local_kb
            ),
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            with_background=True
        )

        self.current_button = event.app.layout.current_window

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)
