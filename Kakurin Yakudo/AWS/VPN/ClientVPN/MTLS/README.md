# MTLS
## ACM
### RSA Gen
```bash
SVR_DNS=
CLI_DNS=
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3

./easyrsa init-pki

./easyrsa --san=DNS:$SVR_DNS build-server-full $SVR_DNS nopass

./easyrsa build-client-full $CLI_DNS nopass
```
### Copy Keys
```bash
mkdir ~/wsi-vpn/
cp pki/ca.crt ~/wsi-vpn/
cp pki/issued/$SVR_DNS.crt ~/wsi-vpn/
cp pki/private/$SVR_DNS.key ~/wsi-vpn/
cp pki/issued/$CLI_DNS.crt ~/wsi-vpn
cp pki/private/$CLI_DNS.key ~/wsi-vpn/
cd ~/wsi-vpn/
```

### ACM Upload
```bash
aws acm import-certificate --certificate fileb://$CLI_DNS.crt --private-key fileb://$CLI_DNS.key --certificate-chain fileb://ca.crt

aws acm import-certificate --certificate fileb://$SVR_DNS.crt --private-key fileb://$SVR_DNS.key --certificate-chain fileb://ca.crt
```
## Client VPN Endpoint