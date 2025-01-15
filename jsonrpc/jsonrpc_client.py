import ssl
import json
import tempfile
import http.client


class JsonRpcClient:
    def __init__(self, host, port, cert, key):
        self.host = host
        self.port = port
        self.cert = cert
        self.key = key

        cert_file = tempfile.NamedTemporaryFile(delete=False)
        key_file = tempfile.NamedTemporaryFile(delete=False)

        try:
            cert_file.write(cert.encode())
            key_file.write(key.encode())
            cert_file.close()
            key_file.close()

            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.load_cert_chain(certfile=cert_file.name, keyfile=key_file.name)
        finally:
            import os
            os.unlink(cert_file.name)
            os.unlink(key_file.name)

    def call_method(self, method, params):
        conn = http.client.HTTPSConnection(self.host, self.port, context=self.context)
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        })
        conn.request("POST", "/api/v2/", payload, headers)
        response = conn.getresponse()
        return json.loads(response.read().decode())
