import json

from prompt_toolkit.layout.dimension import D
from prompt_toolkit.document import Document
from prompt_toolkit.layout import Float
from prompt_toolkit.widgets import Button, TextArea, Dialog, Label
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.key_binding import KeyBindings

from freud.ui.root_container import root_container
from freud.ui.dialog import ErrorDialog
from freud.model import db
from freud.utils import ButtonManager, select_item


class DeleteConfirmation:
    """ Confirm deletion of authentication information """

    def __init__(self, event, dialog):

        def ok_handler():
            root_container.floats.pop()
            db.update_one(values={'name': name,
                                  'auth': None})
            event.app.layout.focus(ButtonManager.prev_button)
            select_item(event)

        def cancel_handler():
            root_container.floats.pop()
            root_container.floats.append(self.auth_float)
            event.app.layout.focus(dialog)

        ok_button = Button(text='OK', handler=ok_handler)
        cancel_button = Button(text='Cancel', handler=cancel_handler)

        name = ButtonManager.current_button

        self.dialog = Dialog(
            title='Delete confirmation',
            body=Label(
                text='Are you sure you want to delete authentication for {}?'
                .format(name)
            ),
            buttons=[cancel_button, ok_button],
            width=D(preferred=80),
            with_background=True
        )

        self.auth_float = root_container.floats.pop()
        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)


class AuthSelector:
    """ Provide selection of authentication types. If the server already has
    authentication, skip selecting and open the respective dialog box """

    def __init__(self, event):

        def dialog_opener(authtype, auth={}):

            if authtype == 'basic':
                BasicAuthDialog(event, auth)
            elif authtype == 'digest':
                DigestAuthDialog(event, auth)

        def ok_handler():

            root_container.floats.pop()

            authtype = self.radio_list.current_value['authtype']
            dialog_opener(authtype)

        def cancel_handler():
            root_container.floats.pop()
            root_container.float_container.key_bindings = None

            event.app.layout.focus(ButtonManager.prev_button)

        kb = KeyBindings()

        server = db.fetch_one(name=ButtonManager.current_button)

        if server.auth:

            auth = json.loads(server.auth)
            auth_type = auth.get('type')
            dialog_opener(auth_type, auth=auth)

        else:

            ok_button = Button(text='OK', handler=ok_handler)
            cancel_button = Button(text='Cancel', handler=cancel_handler)

            self.radio_list = RadioList(values=[
                ({'authtype': 'basic'}, 'Basic'),
                ({'authtype': 'digest'}, 'Digest')
            ])

            kb = self.radio_list.control.key_bindings

            @kb.add('j')
            def down(event):
                self.radio_list._selected_index = min(
                    len(self.radio_list.values) - 1,
                    self.radio_list._selected_index + 1
                )

            @kb.add('k')
            def up(event):
                self.radio_list._selected_index = max(
                    0, self.radio_list._selected_index - 1)

            @kb.add('g', 'g')
            def top(event):
                self.radio_list._selected_index = 0

            @kb.add('G')
            def bottom(event):
                self.radio_list._selected_index = len(
                    self.radio_list.values) - 1

            self.dialog = Dialog(
                title='Select auth type',
                body=self.radio_list,
                buttons=[ok_button, cancel_button],
                width=D(preferred=80),
                with_background=True,
                modal=True)

            root_container.float_container.key_bindings = kb

            root_container.floats.append(Float(self.dialog))
            event.app.layout.focus(self.dialog)


class AuthDialog:
    """ Parent dialog for authentication """

    def __init__(self):

        self.name = ButtonManager.current_button

        self.ok_button = Button(text='OK', handler=self.ok_handler)

        self.cancel_button = Button(
            text='Cancel', handler=self.cancel_handler)

        self.delete_button = Button(
            text='Delete', handler=self.delete_handler)

        self.authuser = TextArea(
            multiline=False
        )

        self.authpass_one = TextArea(
            multiline=False,
            password=True
        )

        self.authpass_two = TextArea(
            multiline=False,
            password=True
        )

    def ok_handler(self):
        authuser = self.authuser.text
        authpass = self.authpass_one.text

        all_fields = all([authuser, authpass])
        empty_fields = not any([authuser, authpass])

        if authpass != self.authpass_two.text:
            ErrorDialog(self.event, title='Password Error',
                        text='Passwords do not match, please try again')

        elif all_fields or empty_fields:

            if all_fields:
                result = db.update_one({
                    'name': self.name,
                    'auth': json.dumps({
                        'user': authuser,
                        'password': authpass,
                        'type': self.authtype
                    })
                })

            elif empty_fields:
                result = db.update_one(values={'name': self.name,
                                               'auth': None})

            if result.get('success'):
                root_container.floats.pop()
                self.event.app.layout.focus(ButtonManager.prev_button)
                select_item(self.event)

            else:
                ErrorDialog(self.event, title='Add/edit server error',
                            text=result.get('errors'))

        else:
            ErrorDialog(self.event, title='Input Error',
                        text='Missing one or more fields.')

    def delete_handler(self):
        DeleteConfirmation(self.event, self.dialog)

    def cancel_handler(self):
        root_container.floats.pop()
        self.event.app.layout.focus(ButtonManager.prev_button)


class BasicAuthDialog(AuthDialog):
    def __init__(self, event, auth):

        super().__init__()

        self.event = event
        self.authtype = 'basic'

        authuser = auth.get('user', '')
        authpass = auth.get('password', '')

        self.authuser.text = authuser
        self.authuser.buffer.document = Document(authuser, len(authuser))

        self.authpass_one.text = authpass
        self.authpass_one.buffer.document = Document(authpass, len(authpass))

        self.authpass_two.text = authpass
        self.authpass_two.buffer.document = Document(authpass, len(authpass))

        self.dialog = Dialog(
            title='Basic Authentication',
            body=HSplit([
                Label(text='Username:\n'),
                self.authuser,
                Window(height=1, char=' '),
                Label(text='Password'),
                self.authpass_one,
                Window(height=1, char=' '),
                Label(text='Retype password'),
                self.authpass_two
            ]),
            buttons=[self.ok_button, self.cancel_button, self.delete_button],
            width=D(preferred=80),
            with_background=True,
            modal=True)

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)


class DigestAuthDialog(AuthDialog):
    def __init__(self, event, auth):

        super().__init__()

        self.event = event
        self.authtype = 'digest'

        authuser = auth.get('user', '')
        authpass = auth.get('password', '')

        self.authuser.text = authuser
        self.authuser.buffer.document = Document(authuser, len(authuser))

        self.authpass_one.text = authpass
        self.authpass_one.buffer.document = Document(authpass, len(authpass))

        self.authpass_two.text = authpass
        self.authpass_two.buffer.document = Document(authpass, len(authpass))

        self.dialog = Dialog(
            title='Digest Authentication',
            body=HSplit([
                Label(text='Username:\n'),
                self.authuser,
                Window(height=1, char=' '),
                Label(text='Password'),
                self.authpass_one,
                Window(height=1, char=' '),
                Label(text='Retype password'),
                self.authpass_two
            ]),
            buttons=[self.ok_button, self.cancel_button, self.delete_button],
            width=D(preferred=80),
            with_background=True,
            modal=True)

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)
