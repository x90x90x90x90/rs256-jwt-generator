# rs256-jwt-generator
Construct JWT tokens with your own RS256 Certs, create the required certs using the following commands

# Create RSA Private Key
openssl genrsa -out jwtRS256.key 2048

# Extract RSA Public Key
openssl rsa -in jwtRS256.key -out jwtRS256.pub -pubout

# Convert to x509 Cert
openssl req -new -x509 -key jwtRS256.key -days 10000 -out jwtRS256.cer

# Extract fingerprint for x5t value
echo $(openssl x509 -in jwtRS256.cer -fingerprint -noout) | sed 's/SHA1 Fingerprint=//g' | sed 's/://g' | xxd -r -ps | base64
