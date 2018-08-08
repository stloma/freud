from prompt_toolkit.layout import HSplit
from prompt_toolkit.widgets import Box

from freud.utils import CustomButton
from freud.utils import ButtonManager
from freud.model import db
from freud import SERVER_WIDTH


def update_servers(sort_by=None, order=None):

    rows = db.fetch_all(sort_by=sort_by, order=order)
    values = []
    for row in rows:
        values.append(row[0])

    return values


class ServerContainer:

    def refresh(self, sort_by=None, order=None):

        names = update_servers(sort_by=sort_by, order=order)

        self.server_list = []
        for name in names:
            button_obj = ButtonManager(name)
            button = CustomButton(name, handler=button_obj.click_handler)
            self.server_list.append(button)

        # If there are no servers
        if not self.server_list:
            from prompt_toolkit.layout.containers import Window
            from prompt_toolkit.layout.controls import FormattedTextControl

            window = Window(
                FormattedTextControl(
                    'No Servers',
                    focusable=True,
                    show_cursor=False
                )
            )

            self.server_list.append(window)

        self.hsplit = HSplit(self.server_list)

        boxes = Box(
            width=SERVER_WIDTH,
            padding_top=0,
            padding_left=1,
            body=self.hsplit
        )

        from freud.key_bindings import server_kb

        self.content = HSplit([
            boxes
        ], key_bindings=server_kb)

        return self.content


servers = ServerContainer()
