import pytest
import json

from freud.api.request import request_handler
from freud.ui.text_buffers import response_box


class TestResponses:

    @pytest.mark.asyncio
    async def test_get_request(self, db_request_data):
        # Need to create response_box here, so response_box.lexer is available
        response_box.create()

        response = await request_handler('httpbin-get')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

    @pytest.mark.asyncio
    async def test_delete_request(self, db_request_data):

        response = await request_handler('httpbin-delete')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

    @pytest.mark.asyncio
    async def test_patch_request(self, db_request_data):

        response = await request_handler('httpbin-patch')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

    @pytest.mark.asyncio
    async def test_post_request(self, db_request_data):

        response = await request_handler('httpbin-post')
        _, output = response.get('response')

        r = json.loads(output)
        post_data = r['data']

        assert post_data == '{"name": "alice"}'

    @pytest.mark.asyncio
    async def test_put_request(self, db_request_data):

        response = await request_handler('httpbin-put')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

    @pytest.mark.asyncio
    async def test_post_form(self, db_request_data):

        response = await request_handler('httpbin-post-form')
        _, output = response.get('response')

        r = json.loads(output)
        form_data = r['form']

        assert form_data['email'] == 'alice@email.com'
        assert form_data['name'] == 'alice'

    @pytest.mark.asyncio
    async def test_basic_auth(self, db_request_data):

        response = await request_handler('httpbin-basic-auth-200')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

        response = await request_handler('httpbin-basic-auth-401')
        headers, _ = response.get('response')

        assert headers.startswith("['401 Unauthorized']")

    @pytest.mark.asyncio
    async def test_digest_auth(self, db_request_data):

        response = await request_handler('httpbin-digest-auth-200')
        headers, _ = response.get('response')

        assert headers.startswith("['200 Ok']")

        response = await request_handler('httpbin-digest-auth-401')
        headers, _ = response.get('response')

        assert headers.startswith("['401 Unauthorized']")
