import six
import json

from prompt_toolkit.application import get_app
from prompt_toolkit.filters import to_filter
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

from freud.model import db
from freud.ui.text_buffers import summary_buffer


class ButtonManager:
    """
    Button logic flows through here. Button Manager saves the current button,
    previous button, list of buttons, and provides a click handler.
    """

    current_button = None
    prev_button = None
    buttons = None

    def __init__(self, name):
        self.name = name

    def click_handler(self):

        result = db.fetch_one(name=self.name)

        output = {
            'name': result.name,
            'method': result.method,
            'url': result.url
        }

        if result.headers:
            output.update({
                'headers': json.loads(result.headers)
            })
        if result.body:
            try:
                body = json.loads(result.body)
            except json.decoder.JSONDecodeError:
                body = str(result.body).splitlines()

            output.update({
                'body': body
            })
        if result.auth:
            auth = json.loads(result.auth)
            output.update({
                'auth': {
                    'type': auth['type'],
                    'user': auth['user']
                }
            })

        summary_buffer.read_only = to_filter(False)
        summary_buffer.text = json.dumps(output, indent=2)
        summary_buffer.read_only = to_filter(True)

        type(self).current_button = self.name

        app = get_app()
        type(self).prev_button = app.layout.current_window

    @classmethod
    def update_buttons(cls, app):

        windows = [w for w in app.layout.find_all_windows()]
        cls.buttons = []
        for window in windows:
            if 'CustomButton' in str(window):
                cls.buttons.append(window)

        if cls.prev_button is None and len(cls.buttons) > 0:
            cls.prev_button = cls.buttons[0]

        return cls.buttons


class SortOrder:
    """ Saves the sort order for reference by application """

    sort_by = None
    order = None


class CustomButton:
    """
    Taken from Python Prompt Toolkit's Button class for customization

    Clickable button.
    :param text: The caption for the button.
    :param handler: `None` or callable. Called when the button is clicked.
    :param width: Width of the button.
    """

    def __init__(self, text, handler=None):
        assert isinstance(text, six.text_type)
        assert handler is None or callable(handler)

        self.text = text
        self.handler = handler
        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=self._get_key_bindings(),
            show_cursor=False,
            focusable=True)

        def get_style():
            if get_app().layout.has_focus(self):
                return 'class:button.focused'

            return 'class:button'

        self.window = Window(
            self.control,
            height=1,
            style=get_style,
            dont_extend_width=True,
            dont_extend_height=True)

    def _get_text_fragments(self):
        text = self.text

        def handler(mouse_event):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self.handler()

        return [
            ('class:button.arrow', '', handler),
            ('class:button.text', text, handler),
            ('class:button.arrow', '', handler),
        ]

    def _get_key_bindings(self):
        kb = KeyBindings()

        @kb.add(' ')
        @kb.add('enter')
        def _(event):
            if self.handler is not None:
                self.handler()

        return kb

    def __pt_container__(self):
        return self.window


def on_startup(app):
    """ Run from __main__ after render """

    ButtonManager.update_buttons(app)
    if not summary_buffer.text:
        # When starting app, select first server if none selected
        select_item(app)


class SingleClick:
    """ Provides mouse click key """

    def __init__(self):
        self.event_type = MouseEventType.MOUSE_UP


def select_item(event):
    """ Simulate mouse click """

    # Don't try to select button if there are none
    if len(ButtonManager.buttons) > 0:

        try:

            event.app.layout.current_window.content.text()[1][2](SingleClick())

        # If app is passed in, rather than event
        except AttributeError:

            event.layout.current_window.content.text()[1][2](SingleClick())
