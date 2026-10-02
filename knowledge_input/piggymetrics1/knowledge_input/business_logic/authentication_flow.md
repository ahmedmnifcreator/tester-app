## Authentication flow

### OAuth2 authorization server
- Implemented in `auth-service`.
- Uses Spring Security OAuth2 with token store and user authentication.
- Exposes `/oauth/authorize`, `/oauth/token`, and `/oauth/check_token`.

### User login and token issuance
- Clients submit credentials to `auth-service`.
- On success, the server returns an OAuth2 access token.
- Access tokens are used by clients to authenticate requests to protected services.

### Token validation
- Resource services validate tokens via `auth-service` and token introspection endpoints.
- `UserController.getUser` returns the authenticated principal to account and statistics services.

### Service-to-service auth
- Services use `server` client credentials when calling other services.
- `AuthClient`, `StatisticsClient`, and internal Feign interceptors attach OAuth2 tokens.
- Service calls require `server` scope or allow `demo` account bypass in some cases.

### Scopes and authorization
- API endpoints may restrict to `server` scope for internal calls.
- `demo` user may have special access patterns for storefront or sample data.
- Access is denied with `403` if the token lacks required scope.

### Security configuration
- `WebSecurityConfig` in `auth-service` configures login, CSRF, and password encoding.
- Resource servers protect endpoints with OAuth2 security filters.
- `UserServiceImpl` loads user details from MongoDB.

### Principal propagation
- Authenticated principal identity is used to fetch `Account` and `Notification` data.
- `account-service` and `statistics-service` rely on principal name to map to account records.
