from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition

from freud.server_control.delete_server import DeleteDialog
from freud.server_control.headers_dialog import HeadersDialog
from freud.server_control.server_dialog import ServerDialog
from freud.utils import ButtonManager, select_item
from freud.ui.text_buffers import (
    response_buffer, header_buffer, summary_buffer)
from freud.server_control.call_editor import (
    update_body, open_response_in_editor)
from freud.server_control.auth_dialog import AuthSelector
from freud.ui.keys import KeyQuickRef
from freud.ui.sort import SortDialog
from freud.api import send_request
from freud.server_control import duplicate_server
from freud import KEYS


kb = KeyBindings()
server_kb = KeyBindings()
response_kb = KeyBindings()
header_kb = KeyBindings()
summary_kb = KeyBindings()
completion = KeyBindings()


@Condition
def is_button():
    """ Filter when there are no buttons """

    return len(ButtonManager.buttons) > 0


# Global Keys
#

@kb.add('c-c', eager=True)
def quit_app(event):
    event.app.exit()


@server_kb.add('c-f')
@response_kb.add('c-f')
def keys_quick_reference(event):
    KeyQuickRef(event)


# Navigation Keys
#

@server_kb.add('tab', filter=is_button)
def go_to_header_from_server(event):
    event.app.layout.focus(header_buffer)


@server_kb.add('s-tab', filter=is_button)
def go_to_summary_from_servers(event):
    event.app.layout.focus(summary_buffer)


@header_kb.add('tab', filter=is_button)
def go_to_response_from_header(event):
    event.app.layout.focus(response_buffer)


@header_kb.add('s-tab', filter=is_button)
def go_to_server_from_header(event):
    event.app.layout.focus(ButtonManager.prev_button)


@response_kb.add('tab', filter=is_button)
def go_to_summary_from_response(event):
    event.app.layout.focus(summary_buffer)


@response_kb.add('s-tab', filter=is_button)
def go_to_headers_from_resposne(event):
    event.app.layout.focus(header_buffer)


@summary_kb.add('tab')
def go_to_servers_from_summary(event, filter=is_button):
    event.app.layout.focus(ButtonManager.prev_button)


@summary_kb.add('s-tab', filter=is_button)
def go_to_response_from_summary(event):
    event.app.layout.focus(response_buffer)


@response_kb.add('h', filter=is_button)
@response_kb.add('left', filter=is_button)
def go_to_servers(event):
    if (len(ButtonManager.buttons) > 0):
        event.app.layout.focus(ButtonManager.prev_button)


@server_kb.add('l', filter=is_button)
@server_kb.add('right', filter=is_button)
def go_to_response(event):
    event.app.layout.focus(response_buffer)


@server_kb.add('g', filter=is_button)
def top_of_list(event):
    """ Adds vi binding to jump to top of server list """

    buttons = ButtonManager.buttons

    event.app.layout.focus(buttons[0])
    ButtonManager.prev_button = buttons[0]
    select_item(event)


@server_kb.add('G', filter=is_button)
def bottom_of_list(event):
    """ Adds vi binding to jump to bottom of server list """

    buttons = ButtonManager.buttons

    event.app.layout.focus(buttons[-1])
    ButtonManager.prev_button = buttons[-1]
    select_item(event)


@server_kb.add('j', filter=is_button)
@server_kb.add('down')
def down_button(event):
    """ Scroll down list of servers in the server_container """

    buttons = ButtonManager.buttons

    current_window = event.app.layout.current_window
    idx = buttons.index(current_window)

    try:
        event.app.layout.focus(buttons[idx + 1])
        ButtonManager.prev_button = buttons[idx + 1]
    except IndexError:
        # If we're at the button item, loop to first item

        event.app.layout.focus(buttons[0])
        ButtonManager.prev_button = buttons[0]

    select_item(event)

@server_kb.add('k', filter=is_button)
@server_kb.add('up')
def up_button(event):
    """ Scroll up list of servers in the server_container """

    buttons = ButtonManager.buttons

    current_window = event.app.layout.current_window
    idx = buttons.index(current_window)

    try:
        event.app.layout.focus(buttons[idx - 1])
        ButtonManager.prev_button = buttons[idx - 1]
    except IndexError:
        # If we're at the top item, loop to last item

        event.app.layout.focus(buttons[-1])
        ButtonManager.prev_button = buttons[-1]

    select_item(event)

# Server control keys
#
@server_kb.add(KEYS['open_response_body'], filter=is_button)
@response_kb.add(KEYS['open_response_body'], filter=is_button)
def open_response(event):
    open_response_in_editor(event)


@server_kb.add(KEYS['sort_servers'], filter=is_button)
def sort(event):
    SortDialog(event)


@server_kb.add(KEYS['new_server'])
def new_server(event):
    ServerDialog(event, create_server=True)


@server_kb.add(KEYS['edit_headers'], filter=is_button)
def new_headers(event):
    HeadersDialog(event)


@server_kb.add(KEYS['edit_server'], filter=is_button)
def edit(event):
    ServerDialog(event)


@server_kb.add(KEYS['edit_authentication'], filter=is_button)
def edit_authentication(event):
    AuthSelector(event)


@server_kb.add(KEYS['edit_body'], filter=is_button)
def edit_body(event):
    update_body(event)


@server_kb.add(KEYS['delete_server'], filter=is_button)
def rm_server(event):
    DeleteDialog(event)


@server_kb.add(KEYS['send_request'], filter=is_button)
def request(event):
    send_request(event)


@server_kb.add(KEYS['duplicate_server'], filter=is_button)
def duplicate(event):
    duplicate_server(event)

