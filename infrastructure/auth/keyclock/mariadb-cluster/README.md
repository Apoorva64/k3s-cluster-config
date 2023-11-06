kubectl create secret generic mariadb-secrets --from-file=mariadb-secrets.yaml --dry-run=client -oyaml -n keycloak > mariadb-secrets-secret.yaml

# seal secret
kubeseal --format=yaml  < mariadb-secrets-secret.yaml > mariadb-secrets-secret-sealed.yaml