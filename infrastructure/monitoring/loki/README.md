### Secret create

```shell
kubectl create secret generic loki-s3-access --from-file=loki-s3-values.yaml --dry-run=client -oyaml -n monitoring > loki-s3-access.yaml

# seal secret
kubeseal --format=yaml  < loki-s3-access.yaml > loki-s3-access-sealed.yaml
```

### grafana

# add datasource

http://loki-read:3100

X-Scope-OrgID: admins