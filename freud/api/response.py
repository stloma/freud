import requests
import json
import xml

from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import HtmlLexer, JsonLexer, XmlLexer

from freud.ui.text_buffers import response_box
from freud import INDENTATION


def response_handler(response):
    # Format content for header_buffer
    #
    status_code_lookup = requests.status_codes._codes
    status_description = status_code_lookup[response.status_code][0]
    status_description = status_description[0].upper(
    ) + status_description[1:]

    seconds = response.elapsed.total_seconds()
    elapsed = str('{}ms'.format(round(seconds * 1000, 2)))

    # if elapsed time is 1 second or greater, display seconds instead of ms
    if (len(elapsed.split('.')[0])) > 3:
        elapsed = str('{}s'.format(round(seconds, 2)))

    status_code = ['{} {}'.format(
        response.status_code, status_description)]

    headers = response.headers

    headers_string = ''
    for k, v in headers.items():
        headers_string += '{}: {}\n'.format(k, v)
    headers_string = headers_string.rstrip('\n')

    headers = '{} | {}\n{}'.format(status_code, elapsed, headers_string)

    response_body = content_type_handler(response)

    # Format content for response_buffer
    #
    return headers, response_body


def content_type_handler(response):

    content_type = response.headers.get('Content-Type')
    response_body = None
    if content_type:

        if content_type.startswith('application/json'):
            try:
                response_body = json.dumps(response.json(), indent=INDENTATION)
                response_box.buffer_control.lexer = PygmentsLexer(
                    JsonLexer)
            except json.decoder.JSONDecodeError as e:
                response_body = 'JSON Error: {}\n\n'.format(str(e))
                response_body += response.text

        elif content_type.startswith('text/html'):
            response_body = response.text
            response_box.buffer_control.lexer = PygmentsLexer(
                HtmlLexer)

        elif content_type.startswith('text/xml'):
            try:
                xml_data = xml.dom.minidom.parseString(response.text)
                response_body = xml_data.toprettyxml(indent=' ' * 2)
                response_box.buffer_control.lexer = PygmentsLexer(
                    XmlLexer)
            except xml.parsers.expat.ExpatError as e:
                response_body = 'XML Error: {}\n\n'.format(str(e))
                response_body += response.text

    if not response_body:
        response_body = response.text

    return response_body
