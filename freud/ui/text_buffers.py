from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.layout.margins import ScrollbarMargin, NumberedMargin
from prompt_toolkit.layout.containers import Window
from pygments.lexers import JsonLexer
from prompt_toolkit.layout import HSplit

from prompt_toolkit.widgets import SearchToolbar

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Keyword, String, Name

from freud import HEADER_HEIGHT, SUMMARY_HEIGHT

response_buffer = Buffer(
    read_only=True, enable_history_search=True, name='response_buffer')
header_buffer = Buffer(read_only=True, name='header_buffer')
summary_buffer = Buffer(read_only=True, name='summary_buffer')

search_toolbar = SearchToolbar()


class HeaderLexer(RegexLexer):
    tokens = {
        'root': [
            (r'(\[)(\')(\d+.*?)(\')(\] )(\| )(\d+.*?\n)',
                bygroups(Keyword, None, Name, None, Keyword, None, Text)),
            (r'(\S+:\s)(.*?$)',
                bygroups(Name, Text))
        ]
    }


class ResponseBox:
    def create(self):
        from freud.key_bindings import response_kb, header_kb

        right_margins = [ScrollbarMargin(display_arrows=True)]
        left_margins = [NumberedMargin()]

        self.buffer_control = BufferControl(
            lexer=PygmentsLexer(JsonLexer),
            search_buffer_control=search_toolbar.control,
            buffer=response_buffer)

        header_window = Window(
            wrap_lines=True,
            right_margins=right_margins,
            left_margins=left_margins,
            height=HEADER_HEIGHT,
            content=BufferControl(
                key_bindings=header_kb,
                search_buffer_control=search_toolbar.control,
                lexer=PygmentsLexer(HeaderLexer), buffer=header_buffer)
        )

        body_window = Window(
            left_margins=left_margins,
            right_margins=right_margins,
            wrap_lines=True,
            content=self.buffer_control
        )

        return HSplit([
            header_window,
            Window(height=1, char='─', style='class:line'),
            body_window,
        ], key_bindings=response_kb)


response_box = ResponseBox()


def summary_box():

    from freud.key_bindings import summary_kb

    return Window(
        content=BufferControl(
            key_bindings=summary_kb,
            lexer=PygmentsLexer(JsonLexer), buffer=summary_buffer
        ), height=SUMMARY_HEIGHT
    )
