#Create ssl directory with subdirectories (certs and keys) to store certificiates and keys
sudo mkdir -p ssl
cd ssl
sudo mkdir -p certs
sudo mkdir -p keys

# Gernerate CA private key and CA certificate
sudo openssl genrsa -aes256 -out cakey.pem 2048
sudo openssl req -x509 -new -nodes -key cakey.pem -sha256 -days 1825 -out cacert.pem -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=ca.pa4.test"

#Display CA Certificate
openssl x509 -text -noout -in cacert.pem

#Move root CA to the directory that the ca-certificate uses and change to ctr.
sudo cp cacert.pem /usr/local/share/ca-certificates/cacert.crt
sudo update-ca-certificates

#Gernerate Web Server's private key and Certificate Signing Request (CSR)
sudo openssl genrsa -out webserver-key.pem 2048
sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -key webserver-key.pem -out webserver.csr -subj "/C=US/ST=California/L=Oakland/O=Nimbus Cloud Services/OU=IT/CN=www.nimbuscloudservices.test"

#Signed certificate for web server
sudo openssl x509 -req -days 365 -in webserver.csr -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out webserver-cert.pem

#Display certificate for web server
openssl x509 -text -noout -in webserver-cert.pem

#Move certificates and keys to the correct subdirectories inside the ssl directory
sudo mv cacert.pem ./certs
sudo mv webserver-cert.pem ./certs
sudo mv cakey.pem ./keys
sudo mv webserver-key.pem ./keys
