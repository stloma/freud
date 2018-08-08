import asyncio

from prompt_toolkit.filters.utils import to_filter

from freud.ui.dialog import LoadingDialog, ErrorDialog
from freud.utils import ButtonManager
from freud.ui.text_buffers import (
    response_buffer, header_buffer)
from freud.api.request import request_handler


def send_request(event):
    """ Prepare and send request, then display the response """

    name = ButtonManager.current_button

    # Display loading dialog
    loading_dialog = LoadingDialog(
        event=event,
        title='Loading',
        text='Connecting to {}...'.format(name)
    )

    async def send_request_async():
        # Cede control of event loop. See:
        # github.com/python/asyncio/issues/284ield
        await asyncio.sleep(0)

        # Build and send request to server
        result = await request_handler(name)

        loading_dialog.close_dialog()

        errors = result.get('errors')

        if errors:
            error_type, error_value = list(errors.items())[0]

            header_buffer.read_only = to_filter(False)
            header_buffer.text = error_type
            header_buffer.read_only = to_filter(True)

            response_buffer.read_only = to_filter(False)
            response_buffer.text = ''
            response_buffer.read_only = to_filter(True)

            # LoadingDialog is not removed if called a second time. Invalidate
            # method sends a repaint trigger
            event.app.invalidate()

            return ErrorDialog(event, title=error_type,
                               text=error_value)

        headers, response_body = result.get('response')

        header_buffer.read_only = to_filter(False)
        header_buffer.text = headers
        header_buffer.read_only = to_filter(True)

        response_buffer.read_only = to_filter(False)
        response_buffer.text = response_body
        response_buffer.read_only = to_filter(True)

    asyncio.ensure_future(send_request_async())
