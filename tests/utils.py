from prompt_toolkit.mouse_events import MouseEventType


class SingleClick:
    def __init__(self):
        self.event_type = MouseEventType.MOUSE_UP
