# Gernerate CA private key and CA certificate
sudo openssl req -x509 -newkey rsa:2048 -days 1825 -keyout cakey.pem -out cacert.pem -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=ca.pa4.test"

#Display CA Certificate
openssl x509 -text -noout -in cacert.pem

#Move root CA to the directory that the ca-certificate uses and change to ctr.
sudo cp cacert.pem /usr/local/share/ca-certificates/cacert.crt

sudo update-ca-certificates

#Gernerate Web Server's private key and Certificate Signing Request (CSR)
sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -newkey rsa:2048 -keyout webserver-key.pem -out webserver.csr -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=www.webpa4.test"

#Signed certificate for web server
sudo openssl x509 -req -days 365 -in webserver.csr -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out webserver-cert.pem

#Display certificate for web server
openssl x509 -text -noout -in webserver-cert.pem
