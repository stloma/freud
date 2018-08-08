import json

from prompt_toolkit.layout.dimension import D
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.widgets import Button, TextArea, Dialog, Label
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout import Float
from prompt_toolkit.key_binding import KeyBindings


from freud.ui.dialog import ErrorDialog
from freud.ui.root_container import root_container
from freud.model import db
from freud.utils import ButtonManager, select_item


headers = [
    'Accept',
    'Accept-Charset',
    'Accept-Encoding',
    'Accept-Language',
    'Accept-Datetime',
    'Authorization',
    'Cache-Control',
    'Connection',
    'Cookie',
    'Content-Length',
    'Content-MD5',
    'Content-Type',
    'Date',
    'Expect',
    'Forwarded',
    'From',
    'Host',
    'If-Match',
    'If-Modified-Since',
    'If-None-Match',
    'If-Range',
    'If-Unmodified-Since',
    'Max-Forwards',
    'Origin',
    'Pragma',
    'Proxy-Authorization',
    'Range',
    'Referer',
    'TE',
    'User-Agent',
    'Upgrade',
    'Via',
    'Warning',
]

header_values = [
    'application/json',
    'text/html'
]

headers_completer = WordCompleter(headers,
                                  ignore_case=True)

header_values_completer = WordCompleter(header_values,
                                        ignore_case=True)


class HeadersDialog:
    def __init__(self, event):

        def ok_handler():
            result = add_headers_to_db(event, name)

            if result.get('success'):
                root_container.floats.pop()
                event.app.layout.focus(ButtonManager.prev_button)
                select_item(event)

        def cancel_handler():
            root_container.floats.pop()
            event.app.layout.focus(ButtonManager.prev_button)

        # Get data about server currently editing
        name = ButtonManager.current_button
        result = db.fetch_one(name=name)

        # Dialog configuration
        ok_button = Button(text='OK', handler=ok_handler)
        cancel_button = Button(text='Cancel', handler=cancel_handler)

        local_kb = KeyBindings()

        @local_kb.add('enter')
        def cancel_completion(event):
            buff = event.app.current_buffer
            buff.complete_state = None
            event.app.layout.focus_next()

        @local_kb.add('c-n')
        def add_header(event):
            new_header = HeaderFactory()
            spacer = Window(height=1, char=' ')
            self.input.children.append(spacer)
            self.input.children.append(new_header.vsplit)

        # Setup initial headings for headers
        self.input = HSplit([
            Label(text='Press ctrl+n to add another header'),
            Window(height=1, char='─'),
            VSplit([
                Label(text='Header'),
                Window(width=1, char=' '),
                Label(text='Type'),
            ]),
            Window(height=1, char=' ')
        ], key_bindings=local_kb)

        # If there are existing headers, include them in the layout
        if result.headers:
            headers = json.loads(result.headers)
            for header in headers:
                new_header = HeaderFactory(
                    header=header, value=headers[header])
                spacer = Window(height=1, char=' ')
                self.input.children.append(spacer)
                self.input.children.append(new_header.vsplit)

        # If there are no headers currently assigned to the server, create
        # empty boxes for input
        else:
            new_header = HeaderFactory()
            spacer = Window(height=1, char=' ')
            self.input.children.append(spacer)
            self.input.children.append(new_header.vsplit)

        self.dialog = Dialog(
            title='Headers',
            body=self.input,
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            with_background=True
        )

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)


class HeaderFactory:

    headers = []

    def __init__(self, header=None, value=None):

        header = header if header else ''
        value = value if value else ''

        self.header = TextArea(
            multiline=False,
            password=False,
            completer=headers_completer,
            text=header
        )
        self.value = TextArea(
            multiline=False,
            password=False,
            completer=header_values_completer,
            text=value
        )
        self.vsplit = VSplit([
            self.header,
            Window(width=1, char=' '),
            self.value,
        ])
        HeaderFactory.headers.append(self)


def add_headers_to_db(event, name):

    headers = {}
    for header in HeaderFactory.headers:
        if header.header.text == '' and header.value.text == '':
            # Skip empty input boxes
            continue

        if headers.get(header.header.text, None):

            ErrorDialog(event, title='Duplicate Header',
                        text='Please remove duplicate header')

            return {'success': False}

        headers[header.header.text] = header.value.text

    if len(headers) == 0:
        # Since there are no headers, set headers to None in db
        result = db.update_one(values={'name': name,
                                       'headers': None})
    else:
        result = db.update_one(values={'name': name,
                                       'headers': json.dumps(headers)})

    # Delete all headers from factory
    HeaderFactory.headers = []

    if result.get('errors'):
        ErrorDialog(event, title='Header error',
                    text=result.get('errors'))

        return {'success': False}

    return {'success': True}
