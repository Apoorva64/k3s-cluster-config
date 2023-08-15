### kubeseal
```bash
 kubeseal --format=yaml  < auth-generic-oauth-secret.yaml > auth-generic-oauth-secret-sealed.yaml
```



### Keycloak steps
- make roles client scope to be included in the token

- add client with
```json
{
  "clientId": "grafana_oauth",
  "name": "",
  "description": "",
  "rootUrl": "https://grafana.monitoring.apoorva64.com/",
  "adminUrl": "",
  "baseUrl": "https://grafana.monitoring.apoorva64.com/",
  "surrogateAuthRequired": false,
  "enabled": true,
  "alwaysDisplayInConsole": true,
  "clientAuthenticatorType": "client-secret",
  "secret": "<redacted>",
  "redirectUris": [
    "https://grafana.monitoring.apoorva64.com/*"
  ],
  "webOrigins": [
    "+"
  ],
  "notBefore": 0,
  "bearerOnly": false,
  "consentRequired": false,
  "standardFlowEnabled": true,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": true,
  "serviceAccountsEnabled": false,
  "publicClient": false,
  "frontchannelLogout": true,
  "protocol": "openid-connect",
  "attributes": {
    "oidc.ciba.grant.enabled": "false",
    "client.secret.creation.time": "1690116141",
    "backchannel.logout.session.required": "true",
    "post.logout.redirect.uris": "+",
    "display.on.consent.screen": "false",
    "oauth2.device.authorization.grant.enabled": "false",
    "backchannel.logout.revoke.offline.tokens": "false"
  },
  "authenticationFlowBindingOverrides": {},
  "fullScopeAllowed": true,
  "nodeReRegistrationTimeout": -1,
  "defaultClientScopes": [
    "web-origins",
    "acr",
    "roles",
    "profile",
    "groups",
    "email"
  ],
  "optionalClientScopes": [
    "address",
    "phone",
    "offline_access",
    "microprofile-jwt"
  ],
  "access": {
    "view": true,
    "configure": true,
    "manage": true
  }
}
```


## Creating ServiceMonitor

Don't forget to add the label `release: kube-prometheus-stack` to the namespace where you want to monitor the services.

and to the ServiceMonitor add the label `release: kube-prometheus-stack`

