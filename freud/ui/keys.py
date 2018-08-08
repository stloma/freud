from prompt_toolkit.layout.dimension import D
from prompt_toolkit import HTML
from prompt_toolkit.widgets import Button, Dialog, Label
from prompt_toolkit.layout.containers import (
    VSplit, HSplit, Window, HorizontalAlign)
from prompt_toolkit.layout import Float

from freud.utils import ButtonManager
from freud.ui.root_container import root_container
from freud.ui.server_container import servers
from freud import KEYS


class KeyQuickRef:

    """ Displays a quick reference for key bindings """

    def __init__(self, event):

        def ok_handler():

            root_container.floats.pop()
            if ButtonManager.prev_button:
                event.app.layout.focus(ButtonManager.prev_button)
            else:
                event.app.layout.focus(servers.content)

        ok_button = Button(text='OK', handler=ok_handler)

        # Create dialog with title
        self.input = HSplit([
            Label(text=HTML(
                'Default Vi key bindings.')
            ),
            Window(height=1, char=' ')
        ])

        # Add navigation keys to dialog
        self.input.children.append(VSplit([
            Label(text=HTML('<b>Basic navigation</b>\n'))])
        )
        for key in navigation_keys:
            new_key = KeyFactory(
                key=key, value=navigation_keys[key])
            self.input.children.append(new_key.vsplit)

        spacer = Window(height=1, char='─')
        blank_spacer = Window(height=1, char=' ')

        self.input.children.append(blank_spacer)
        self.input.children.append(spacer)

        # Add server keys to dialog
        self.input.children.append(VSplit([
            Label(text=HTML('<b>Server keys</b>\n'))])
        )
        for key in server_keys:
            new_key = KeyFactory(
                key=key, value=server_keys[key])
            self.input.children.append(new_key.vsplit)

        self.input.children.append(blank_spacer)
        self.input.children.append(spacer)

        # Add response keys to dialog
        self.input.children.append(VSplit([
            Label(
                text=HTML(
                    '<b>Text areas (response, headers, summary)</b>\n'))])
        )
        for key in response_body_keys:
            new_key = KeyFactory(
                key=key, value=response_body_keys[key])
            self.input.children.append(new_key.vsplit)
        self.input.children.append(blank_spacer)
        self.input.children.append(blank_spacer)

        self.dialog = Dialog(
            title='Key Quick Reference',
            body=self.input,
            buttons=[ok_button],
            width=D(preferred=80),
            with_background=True,
            modal=True)

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)


class KeyFactory:

    def __init__(self, key=None, value=None):

        self.key = Label(
            text=key,
            width=20
        )
        self.value = Label(
            text=value,
        )
        self.vsplit = VSplit([
            self.key,
            Window(width=1, char=' '),
            self.value
        ], align=HorizontalAlign.LEFT)


# leader = KEYS['leader']

navigation_keys = {
    'tab': 'Switch windows',
    'j/down': 'Next server',
    'k/up': 'Previous server',
    'g': 'First server',
    'G': 'Last server',
}

server_keys = {
    KEYS['send_request']: 'Send request',
    KEYS['new_server']: 'New server',
    KEYS['edit_server']: 'Edit server',
    KEYS['edit_headers']: 'Edit headers',
    KEYS['edit_authentication']: 'Edit auth',
    KEYS['edit_body']: 'Edit body',
    KEYS['delete_server']: 'Delete server',
}

response_body_keys = {
    '/': 'Forward search',
    '?': 'Backward search',
    'n/N': 'Next/Previous search term',
    'Vi Navigation': 'e.g., gg, G, ctrl+u, ctrl+d, etc.',
}
