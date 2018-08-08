import json
from prompt_toolkit.layout.layout import Layout
from .utils import SingleClick
from freud.utils import ButtonManager
from freud.ui.server_container import servers
from freud.ui.root_container import root_container
from freud.key_bindings import server_kb


class TestChangingLayout:

    @staticmethod
    def _get_windows(root_container):
        root_container = root_container.create()
        layout = Layout(root_container)
        all_windows = layout.find_all_windows()
        windows = []
        for window in all_windows:
            windows.append(window)

        return windows

    @staticmethod
    def _get_all_windows(layout):
        return [w for w in layout.find_all_windows()]

    def test_check_layout(self, db_dummy_data):

        windows = self._get_windows(root_container)

        search_buffer = windows[0]
        title_window = windows[1]
        dummy_one = windows[4]
        button_one = windows[5]
        button_two = windows[6]
        dummy_two = windows[7]
        header_buffer = windows[10]
        response_buffer = windows[12]
        summary_buffer = windows[14]

        assert 'SearchBuffer' in str(search_buffer)
        assert 'Freud' in str(title_window)
        assert 'CustomButton' not in str(dummy_one)
        assert 'CustomButton' in str(button_one)
        assert 'CustomButton' in str(button_two)
        assert 'CustomButton' not in str(dummy_two)
        assert 'header_buffer' in str(header_buffer)
        assert 'response_buffer' in str(response_buffer)
        assert 'summary_buffer' in str(summary_buffer)

    def test_update_response_box(self, db_dummy_data):

        # Create layout
        layout = Layout(root_container.create(),
                        focused_element=servers.content)

        summary_buffer = layout.get_buffer_by_name('summary_buffer')

        # Simulate mouse click on first server
        layout.current_window.content.text()[1][2](SingleClick())
        summary_buffer_before = json.loads(summary_buffer.text)

        # Get buttons for focus
        app = App(layout)
        ButtonManager.update_buttons(app)

        # Focus and simulate click on next server
        layout.focus(ButtonManager.buttons[1])
        layout.current_window.content.text()[1][2](SingleClick())
        summary_buffer_after = json.loads(summary_buffer.text)

        assert summary_buffer_before['name'] == 'alice'
        assert summary_buffer_after['name'] == 'bob'

    def test_add_server(self, db, db_dummy_data):
        db.add_one({'name': 'john', 'url': 'john.com', 'method': 'get'})

        windows = self._get_windows(root_container)

        dummy_one = windows[4]
        button_one = windows[5]
        button_two = windows[6]
        button_three = windows[7]
        dummy_two = windows[8]

        assert 'CustomButton' not in str(dummy_one)
        assert 'CustomButton' in str(button_one)
        assert 'CustomButton' in str(button_two)
        assert 'CustomButton' in str(button_three)
        assert 'CustomButton' not in str(dummy_two)

    def test_delete_server(
            self, db, db_dummy_data):

        # Get handler for delete server key binding
        for key in server_kb.bindings:
            if 'rm_server' in str(key):
                delete_handler = key.handler

        # Create layout
        root = root_container.create()
        layout = Layout(root,
                        focused_element=servers.content)
        windows = self._get_all_windows(layout)

        event = Event(layout)

        # Simulate mouse click on first server
        layout.current_window.content.text()[1][2](SingleClick())

        # Simulate pressing key binding for deleting a server
        delete_handler(event)

        # When a server is deleted in the app we get a delete confirmation
        # dialog, which is stored in root.floats. Check for that
        # here.
        windows = self._get_all_windows(layout)
        floats = root.floats

        assert len(floats) == 2

        # Simulate pressing the OK button in the delete confirmation dialog
        windows[34].content.text()[1][2](SingleClick())

        assert len(floats) == 1

        windows = self._get_all_windows(layout)

        dummy_one = str(windows[4])
        button_one = str(windows[5])
        dummy_two = str(windows[6])

        assert 'Button' not in dummy_one
        assert 'Button' in button_one
        assert 'Button' not in dummy_two

    def test_sort_dialog(self, db_dummy_data):

        for key in server_kb.bindings:
            if 'sort' in str(key):
                sort_handler = key.handler

        # Create layout
        root = root_container.create()
        layout = Layout(root,
                        focused_element=servers.content)
        windows = self._get_all_windows(layout)

        assert len(root_container.floats) == 1

        event = Event(layout)
        sort_handler(event)

        assert len(root_container.floats) == 2

        windows = self._get_all_windows(layout)
        windows[33].content.text()[1][2](SingleClick())

        assert len(root_container.floats) == 1


class Event:
    def __init__(self, layout):
        self.app = App(layout)
        self.event = self.app


class App:
    def __init__(self, layout):
        self.layout = layout
