| Method | URL | Microservice | Controller | Description | Request body | Response body | Status codes | Authentication required | Related business feature |
|---|---|---|---|---|---|---|---|---|---|
| GET | `/accounts/{name}` | account-service | `AccountController.getAccountByName` | Retrieve account by name | none | `Account` | 200, 401, 403, 404 | yes, `server` scope or `demo` name | account retrieval |
| GET | `/accounts/current` | account-service | `AccountController.getCurrentAccount` | Retrieve current authenticated user account | none | `Account` | 200, 401 | yes | account retrieval |
| PUT | `/accounts/current` | account-service | `AccountController.saveCurrentAccount` | Save current authenticated user account | `Account` | none | 204, 400, 401 | yes | account update |
| POST | `/accounts/` | account-service | `AccountController.createNewAccount` | Create new account and corresponding auth user | `User` | `Account` | 201, 400, 401, 409 | no | account creation |
| GET | `/users/current` | auth-service | `UserController.getUser` | Return authenticated user principal | none | `Principal` | 200, 401 | yes | auth validation |
| POST | `/users` | auth-service | `UserController.createUser` | Create new authentication user | `User` | none | 201, 400, 401, 403 | yes, `server` scope | user creation |
| GET | `/statistics/current` | statistics-service | `StatisticsController.getCurrentAccountStatistics` | Retrieve statistics for current authenticated user | none | `List<DataPoint>` | 200, 401 | yes | statistics retrieval |
| GET | `/statistics/{accountName}` | statistics-service | `StatisticsController.getStatisticsByAccountName` | Retrieve statistics by account name | none | `List<DataPoint>` | 200, 401, 403 | yes, `server` scope or `demo` name | statistics retrieval |
| PUT | `/statistics/{accountName}` | statistics-service | `StatisticsController.saveAccountStatistics` | Save account statistics data | `Account` | none | 204, 400, 401, 403 | yes, `server` scope | statistics update |
| GET | `/recipients/current` | notification-service | `RecipientController.getCurrentNotificationsSettings` | Get notification settings for current account | none | `Recipient` | 200, 401 | yes | notification settings |
| PUT | `/recipients/current` | notification-service | `RecipientController.saveCurrentNotificationsSettings` | Save notification settings for current account | `Recipient` | `Recipient` | 200, 400, 401 | yes | notification settings |
