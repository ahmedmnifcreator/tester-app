## Account service workflow

### Account creation
- Client calls `POST /accounts/` in `account-service`.
- `AccountController.createNewAccount` validates the request and calls `accountService.createAccount`.
- `AccountServiceImpl.createAccount` converts the request into an `Account` domain object.
- It saves the new account in `AccountRepository`.
- It creates a new `User` record in `auth-service` via `AuthClient`.
- Account creation triggers `/statistics/{accountName}` update or initialization.

### Current account retrieval
- Client calls `GET /accounts/current`.
- Controller obtains security principal from request.
- `AccountServiceImpl.getCurrentAccount` loads the authenticated account from MongoDB.
- If no account exists, an appropriate error or empty response is returned.

### Account updates
- Client calls `PUT /accounts/current` with updated `Account` data.
- The controller requires authentication and forwards the body to service.
- `AccountServiceImpl.saveCurrentAccount` validates and updates the account document.
- The service may propagate saved account data to linked statistics and notification logic.

### Account deletion / edge cases
- Deletion is not explicitly provided in the REST API.
- Service handles missing accounts by returning `404` or `403` as appropriate.

### Auth integration
- `account-service` uses `AuthClient` to call `auth-service` user APIs.
- The account and auth user share the same account name / username.
- Auth calls require `server` client credentials in most cases.

### Error handling
- Conflicts when account already exists return `409`.
- Validation errors return `400`.
- Unauthorized requests return `401`.
- Service-to-service requests use OAuth2 tokens and may return `403` for forbidden operations.
