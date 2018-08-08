import tempfile
from subprocess import call
import os

from freud.utils import select_item
from freud.ui.text_buffers import response_buffer, header_buffer
from freud.ui.dialog import ErrorDialog
from freud.model import db
from freud.utils import ButtonManager


def update_body(event):
    """Uses external editor to create/update request body."""

    EDITOR = os.environ.get('EDITOR', None)

    if not EDITOR:
        return ErrorDialog(
            event, title='Error',
            text='Please set your $EDITOR environement variable'
        )

    tf = tempfile.NamedTemporaryFile()

    name = ButtonManager.current_button

    result = db.fetch_one(name=name)

    if result.body:
        with open(tf.name, 'w') as fout:
            fout.write(result.body)

    j = "+'set ft=json"

    call([EDITOR, j, tf.name])

    with open(tf.name, 'r') as fin:
        body = fin.read()

    db.update_one(values={'name': name,
                          'body': body})

    event.app.reset()
    select_item(event)


def open_response_in_editor(event):

    EDITOR = os.environ.get('EDITOR', None)

    if not EDITOR:
        return ErrorDialog(
            event, title='Error',
            text='Please set your $EDITOR environement variable'
        )

    tf = tempfile.NamedTemporaryFile()

    headers = header_buffer.text
    response = response_buffer.text

    set_filetype = None
    if 'content-type: application/json' in headers.lower():
        set_filetype = 'json'
    elif 'text/html' in headers.lower():
        set_filetype = 'html'

    with open(tf.name, 'w') as fout:
        fout.write(str(response))

    if set_filetype:
        call([EDITOR, '+set ft={}'.format(set_filetype), tf.name])
    else:
        call([EDITOR, tf.name])

    event.app.reset()
