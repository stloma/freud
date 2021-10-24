from freud.utils import ButtonManager, select_item
from freud.model import db
from freud.ui.root_container import root_container
from prompt_toolkit.layout import Layout
from freud.ui.dialog import ErrorDialog


def duplicate_server(event):

    name = ButtonManager.current_button
    new_name = name + ' copy'
    result = db.fetch_one(name=name)

    result = db.add_one(
                values={
                    'name': new_name,
                    'url': result.url,
                    'method': result.method,
                    'body': result.body,
                    'auth': result.auth,
                    'headers': result.headers
                })

    if result.get('success'):
        event.app.layout = Layout(root_container.create())
        buttons = ButtonManager.update_buttons(event.app)
        for button in buttons:
            if new_name == button.content.text()[1][1].strip():
                event.app.layout.focus(button)
                break

        select_item(event)

    else:
        # Add/update server returned an error
        ErrorDialog(event, title='Duplicate server error',
                    text=str(result.get('errors')))

