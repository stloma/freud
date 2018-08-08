from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Button
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.widgets import Dialog
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.layout import Float
from prompt_toolkit.layout.controls import FormattedTextControl

from freud.ui.root_container import root_container
from freud.utils import ButtonManager


class ErrorDialog:
    def __init__(self, event, title='', text=''):

        def ok_handler():
            root_container.floats.pop()

            # If there was an original dialog, insert it back into layout
            if self.orig_dialog:
                root_container.floats.append(self.orig_dialog)
                event.app.layout.focus(root_container.float_container)
            else:
                event.app.layout.focus(ButtonManager.prev_button)

        ok_button = Button(text='OK', handler=ok_handler)

        dialog = Dialog(
            Window(
                wrap_lines=True,
                content=FormattedTextControl(text=text),
                always_hide_cursor=True
            ),
            title=title,
            width=D(preferred=80),
            buttons=[ok_button],
            with_background=True
        )

        try:
            # If a dialog was already up, save it
            self.orig_dialog = root_container.floats.pop()
        except IndexError:
            self.orig_dialog = None

        root_container.floats.append(Float(content=dialog))
        event.app.layout.focus(ok_button)


class LoadingDialog:

    """ Displays a loading message when waiting for a server response """

    def __init__(
            self, event=None, title='', text=''):

        content = Window(
            height=3,
            align=WindowAlign.CENTER,
            content=FormattedTextControl(
                text=text,
                show_cursor=False,
                modal=True
            )
        )

        body = HSplit([
            Window(height=1, char=' '),
            content,
            Window(height=1, char=' '),
        ], padding=1)

        dialog = Dialog(
            body,
            title=title,
            width=D(preferred=80),
            with_background=True
        )

        loading_float = Float(content=dialog)

        root_container.floats.append(loading_float)

        self.focus = event.app.layout.focus
        self.focus(content)

    def close_dialog(self):
        root_container.floats.pop()
        self.focus(ButtonManager.prev_button)
