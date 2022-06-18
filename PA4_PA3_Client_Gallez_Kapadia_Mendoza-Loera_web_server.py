import ssl
import http.server


def main():
    # Variables you can modify
    server_address = "www.nimbuscloudservices.test"
    server_port = 4443
    ssl_key_file = "./ssl/keys/webserver-key.pem"
    ssl_certificate_file = "./ssl/certs/webserver-cert.pem"

    # Don't modify anything below
    httpd = http.server.HTTPServer((server_address, server_port), http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   keyfile=ssl_key_file,
                                   certfile=ssl_certificate_file,
                                   ssl_version=ssl.PROTOCOL_TLSv1_2)

    print("Listening on port", server_port)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
