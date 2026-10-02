## Notification processing

### Recipient settings
- `notification-service` stores `Recipient` documents keyed by `accountName`.
- Each recipient includes email, active flag, frequency, and `lastNotified` timestamp.
- Notification settings are updated via `PUT /recipients/current`.

### Scheduled reminders
- Service uses scheduled tasks to evaluate notification frequency and readiness.
- It identifies recipients with `active=true` and due notification intervals.
- Emails are sent using `EmailServiceImpl` when a recipient is ready.

### Backup and restore
- Notification service may include backup tasks for recipient settings.
- Backup files or messages can be sent to external storage, though exact backup flow depends on service implementation.

### Service dependencies
- Notifications depend on the authenticated account and recipient mapping.
- They may use account metadata to personalize notification content.

### Error handling
- If email delivery fails, the service logs the failure and retries on the next scheduled run.
- Invalid recipient updates return `400`.
