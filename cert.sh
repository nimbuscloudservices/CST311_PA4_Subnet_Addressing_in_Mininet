# Gernerate CA private key and CA certificate
openssl req -x509 -newkey rsa:2048 -days 1825 -keyout cakey.pem -out cacert.pem -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=ca.pa4.test"

#Display CA Certificate
openssl x509 -text -noout -in cacert.pem

#Gernerate Web Server's private key and Certificate Signing Request (CSR)
openssl req -nodes -new -config /etc/ssl/openssl.cnf -newkey rsa:2048 -keyout webserver-key.pem -out webserver-req.pem -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=www.webpa4.test"

#Signed certificate for web server
openssl x509 -req -days 365 -in webserver-req.pem -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out webserver-cert.pem

#Display certificate for web server
openssl x509 -text -noout -in webserver-cert.pem
