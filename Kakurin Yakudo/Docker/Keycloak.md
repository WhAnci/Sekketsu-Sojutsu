# Keycloak on docker
```bash
export KEYCLOAK_DEV_ADMIN_PASSWORD=Skill53##

docker run -d \
  --name keycloak-dev \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=$KEYCLOAK_DEV_ADMIN_PASSWORD \
  -e KC_PROXY_HEADERS=xforwarded \
  quay.io/keycloak/keycloak:latest \
  start-dev

docker exec -it keycloak-dev bash

# 접속해서 1분정도 대기 후 진행
export PATH=$PATH:/opt/keycloak/bin
kcadm.sh config credentials --server http://localhost:8080/ --realm master --user admin --password Skill53##
kcadm.sh update realms/master -s sslRequired=NONE

kcadm.sh get realms/master
```