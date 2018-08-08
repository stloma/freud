from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.layout import Float
from prompt_toolkit.layout.menus import CompletionsMenu

from freud.ui.body_container import titled_body
from freud.utils import SortOrder


class RootContainer:

    def create(self):

        sort_by = SortOrder.sort_by
        order = SortOrder.order

        self.body = titled_body.create(sort_by=sort_by, order=order)

        self.container = HSplit([self.body])

        completions = Float(xcursor=True,
                            ycursor=True,
                            content=CompletionsMenu(max_height=16, scroll_offset=1))

        self.float_container = FloatContainer(
            content=self.container, floats=[completions])

        self.floats = self.float_container.floats

        return self.float_container


root_container = RootContainer()
