# Istio
## Install
### Install istioctl
```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.29.1
export PATH=$PWD/bin:$PATH
```
### Install
```bash
istioctl install
# This will install the Istio 1.29.1 profile "default" into the cluster. Proceed? (y/N): y
```
### Uninstall
```bash
istioctl uinstll
# Proceed? (y/N): y