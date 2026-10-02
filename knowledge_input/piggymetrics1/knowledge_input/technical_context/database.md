## Database technology
- MongoDB is used for persistence in `auth-service`, `account-service`, `statistics-service`, and `notification-service`.
- Each service uses its own MongoDB instance.

## Collections
- `auth-service`: `users`
- `account-service`: `accounts`
- `statistics-service`: `datapoints`
- `notification-service`: `recipients`

## Domain models
- `auth-service.User`
  - `username` (ID)
  - `password`
- `account-service.Account`
  - `name` (ID)
  - `lastSeen`
  - `incomes`
  - `expenses`
  - `saving`
  - `note`
- `account-service.Item`
  - `title`, `amount`, `currency`, `period`, `icon`
- `account-service.Saving`
  - `amount`, `currency`, `interest`, `deposit`, `capitalization`
- `statistics-service.DataPoint`
  - `id` (`DataPointId`), `incomes`, `expenses`, `statistics`, `rates`
- `statistics-service.DataPointId`
  - `account`, `date`
- `notification-service.Recipient`
  - `accountName` (ID), `email`, `scheduledNotifications`
- `notification-service.NotificationSettings`
  - `active`, `frequency`, `lastNotified`

## Relationships
- Account and User are linked by username but stored separately.
- Statistics datapoints are linked to account name.
- Notification recipient settings are linked to account name.
- Relationships are application-managed rather than enforced by MongoDB foreign keys.

## Repository classes
- `auth-service.UserRepository`
- `account-service.AccountRepository`
- `statistics-service.DataPointRepository`
- `notification-service.RecipientRepository`

## Persistence layer
- Spring Data MongoDB provides repository implementations.
- Documents use `@Document(collection = ...)`.
- IDs use `@Id` fields.
- `statistics-service` includes custom converters for `DataPointId`.

## Data flow
- `account-service` creates accounts and triggers statistics updates.
- `auth-service` stores user credentials.
- `statistics-service` stores daily financial datapoints.
- `notification-service` stores recipient settings and retrieves ready-to-notify recipients.

## Database initialization
- `account-mongodb` uses `INIT_DUMP: account-service-dump.js`.
- Tests use embedded MongoDB via `de.flapdoodle.embed.mongo`.

## Data ownership by service
- `auth-service` owns user authentication data.
- `account-service` owns account and transaction data.
- `statistics-service` owns statistics datapoints.
- `notification-service` owns recipient notification settings.
