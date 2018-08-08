import asyncio

from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.eventloop import use_asyncio_event_loop

from freud.key_bindings import kb
from freud.ui.server_container import servers
from freud.ui.root_container import root_container
from freud.ui.style import style
from freud.utils import on_startup


use_asyncio_event_loop()


def main():
    app = Application(
        layout=Layout(root_container.create(),
                      focused_element=servers.content),
        key_bindings=kb,
        editing_mode=EditingMode.VI,
        style=style,
        mouse_support=True,
        full_screen=True,
        after_render=on_startup
    )

    asyncio.get_event_loop().run_until_complete(
        app.run_async().to_asyncio_future()
    )
