from prompt_toolkit.layout.containers import (
    VSplit, HSplit, Window, WindowAlign)
from prompt_toolkit.layout.controls import FormattedTextControl

from freud.ui.text_buffers import response_box, summary_box, search_toolbar
from freud.ui.server_container import servers
from freud import __version__


class TitledBody:

    def create(self, sort_by=None, order=None):

        self.servers = servers.refresh(sort_by=sort_by, order=order)

        servers_output = VSplit([
            self.servers,
            Window(width=1, char='│', style='class:line'),
            response_box.create(),
        ])

        body = HSplit([
            servers_output,
            Window(height=1, char='─', style='class:line'),
            summary_box()
        ])

        title_bar = [
            ('class:title', ' Freud {}'.format(__version__)),
            ('class:title',
             ' (Press [Ctrl-C] to quit. Press [Ctrl-F] for info.)'),
        ]

        self.container = HSplit([
            search_toolbar,
            Window(height=1,
                   content=FormattedTextControl(title_bar),
                   align=WindowAlign.CENTER),
            Window(height=1, char='─', style='class:line'),
            body,
        ])

        return self.container


titled_body = TitledBody()
