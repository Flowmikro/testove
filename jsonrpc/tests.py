import unittest
from unittest.mock import patch, MagicMock

from django.conf import settings

from .jsonrpc_client import JsonRpcClient


class TestJsonRpcClient(unittest.TestCase):

    @patch('http.client.HTTPSConnection')
    def test_call_method_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"jsonrpc": "2.0", "result": "success", "id": 1}'
        mock_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = JsonRpcClient('slb.medv.ru', 443, settings.CERTIFICATE, settings.PRIVATE_KEY)
        result = client.call_method('test.method', {'param1': 'value1'})

        self.assertEqual(result, {"jsonrpc": "2.0", "result": "success", "id": 1})

    @patch('http.client.HTTPSConnection')
    def test_call_method_failure(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = (
            b'{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 1}'
        )

        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = JsonRpcClient('slb.medv.ru', 443, settings.CERTIFICATE, settings.PRIVATE_KEY)
        result = client.call_method('non.existent.method', {})

        self.assertEqual(result, {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": 1})
