from prompt_toolkit.layout import Float
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import Button, Dialog, Label
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.filters import to_filter

from freud.model import db
from freud.ui.root_container import root_container
from freud.utils import ButtonManager, select_item
from freud.ui.server_container import servers
from freud.ui.text_buffers import summary_buffer


class DeleteDialog:
    def __init__(self, event):

        def ok_handler():
            # if len(ButtonManager.buttons) > 0:
            delete_server(event, name)
            root_container.floats.pop()

        def cancel_handler():
            root_container.floats.pop()
            event.app.layout.focus(ButtonManager.prev_button)

        # Get data about server currently editing
        name = ButtonManager.current_button

        # Dialog configuration
        ok_button = Button(text='OK', handler=ok_handler)
        cancel_button = Button(text='Cancel', handler=cancel_handler)

        self.dialog = Dialog(
            title='Delete confirmation',
            body=Label(
                text='Are you sure you want to delete {}?'.format(name)),
            buttons=[cancel_button, ok_button],
            width=D(preferred=80),
            with_background=True
        )

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)


def delete_server(event, name):

    db.delete_one(name)

    buttons = servers.hsplit.children

    # The server has been removed from the db. Now, we have to remove the
    # button from the layout by iterating over buttons and removing it by index
    for idx, button in enumerate(buttons):
        if name == button.content.text()[1][1].strip():

            del buttons[idx]

            if len(buttons) > 0:

                try:
                    # If the deleted button was not the last button
                    event.app.layout.focus(buttons[idx])
                    ButtonManager.prev_button = buttons[idx]
                    select_item(event)

                except IndexError:
                    # If the deleted button was the last button
                    event.app.layout.focus(buttons[idx - 1])
                    ButtonManager.prev_button = buttons[idx - 1]
                    select_item(event)

            else:
                # Last button was deleted, display message "No servers"

                control = FormattedTextControl(
                    'No Servers',
                    focusable=True,
                    show_cursor=False)

                window = Window(
                    control,
                    height=1,
                    dont_extend_width=True,
                    dont_extend_height=True)

                buttons.append(window)

                summary_buffer.read_only = to_filter(False)
                summary_buffer.text = ''
                summary_buffer.read_only = to_filter(True)

                ButtonManager.prev_button = None
                ButtonManager.current_button = None

                event.app.layout.focus(servers.content)
