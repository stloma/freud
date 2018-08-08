from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout import Float
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Button, Dialog, RadioList
from prompt_toolkit.key_binding import KeyBindings

from freud.utils import ButtonManager, SortOrder
from freud.ui.root_container import root_container
from freud.ui.server_container import servers


class SortDialog:
    def __init__(self, event):
        kb = KeyBindings()

        def ok_handler():

            sort_by = self.radio_list.current_value['sort_by']
            order = self.radio_list.current_value['order']

            SortOrder.sort_by = sort_by
            SortOrder.order = order

            root_container.floats.pop()

            event.app.layout = Layout(root_container.create(),
                                      focused_element=servers.content
                                      )
            ButtonManager.prev_button = event.app.layout.current_window

        def cancel_handler():
            root_container.floats.pop()
            root_container.float_container.key_bindings = None
            event.app.layout.focus(ButtonManager.prev_button)

        ok_button = Button(text='OK', handler=ok_handler)
        cancel_button = Button(text='Cancel', handler=cancel_handler)

        self.radio_list = RadioList(values=[
            ({'sort_by': 'name', 'order': 'asc'}, 'Name'),
            ({'sort_by': 'name', 'order': 'desc'}, 'Name - Desc'),
            ({'sort_by': 'timestamp', 'order': 'asc'}, 'Time Added'),
            ({'sort_by': 'timestamp', 'order': 'desc'}, 'Time Added - Desc')
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
            self.radio_list._selected_index = len(self.radio_list.values) - 1

        self.dialog = Dialog(
            title='Sort',
            body=self.radio_list,
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            with_background=True,
            modal=True)

        root_container.float_container.key_bindings = kb

        root_container.floats.append(Float(self.dialog))
        event.app.layout.focus(self.dialog)
