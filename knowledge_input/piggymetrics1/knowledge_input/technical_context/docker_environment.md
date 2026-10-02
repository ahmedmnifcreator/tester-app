## Docker Compose architecture
PiggyMetrics uses Docker Compose to orchestrate a config server, registry, gateway, backend services, MongoDB instances, RabbitMQ, monitoring, and Turbine stream service.

## Containers
- `rabbitmq`
- `config`
- `registry`
- `gateway`
- `auth-service`
- `auth-mongodb`
- `account-service`
- `account-mongodb`
- `statistics-service`
- `statistics-mongodb`
- `notification-service`
- `notification-mongodb`
- `monitoring`
- `turbine-stream-service`

## Images
Production compose uses:
- `rabbitmq:3-management`
- `sqshq/piggymetrics-config`
- `sqshq/piggymetrics-registry`
- `sqshq/piggymetrics-gateway`
- `sqshq/piggymetrics-auth-service`
- `sqshq/piggymetrics-mongodb`
- `sqshq/piggymetrics-account-service`
- `sqshq/piggymetrics-statistics-service`
- `sqshq/piggymetrics-notification-service`
- `sqshq/piggymetrics-monitoring`
- `sqshq/piggymetrics-turbine-stream-service`

Development compose builds locally from project folders:
- `config`, `registry`, `gateway`, `auth-service`, `mongodb`, `account-service`, `statistics-service`, `notification-service`, `monitoring`, `turbine-stream-service`

## Ports
Production compose maps:
- `15672:15672` RabbitMQ management
- `8761:8761` Eureka registry
- `80:4000` Gateway
- `9000:8080` Monitoring
- `8989:8989` Turbine stream

Development compose maps:
- `5672:5672` RabbitMQ
- `8888:8888` Config server
- `5000:5000` Auth service
- `25000:27017` Auth MongoDB
- `6000:6000` Account service
- `26000:27017` Account MongoDB
- `7000:7000` Statistics service
- `27000:27017` Statistics MongoDB
- `8000:8000` Notification service
- `28000:27017` Notification MongoDB

## Networks
- Compose uses the default network
- Services resolve each other by container name

## Environment variables
Set in `.env`:
- `CONFIG_SERVICE_PASSWORD`
- `NOTIFICATION_SERVICE_PASSWORD`
- `STATISTICS_SERVICE_PASSWORD`
- `ACCOUNT_SERVICE_PASSWORD`
- `MONGODB_PASSWORD`

Passed into services for configuration and secrets.

## Mounted volumes
- No explicit volume mounts in compose files
- MongoDB container `account-mongodb` uses `INIT_DUMP: account-service-dump.js` for initialization

## Dependencies
Production compose defines dependencies:
- `registry` depends on `config`
- `gateway`, `auth-service`, `account-service`, `statistics-service`, `notification-service`, `monitoring`, and `turbine-stream-service` depend on `config`

Development compose uses local build and no explicit `depends_on` beyond service definitions.

## Startup order
1. `rabbitmq`
2. `config`
3. `registry`
4. `gateway`
5. `auth-service`
6. `account-service`
7. `statistics-service`
8. `notification-service`
9. `monitoring`
10. `turbine-stream-service`

## Health checks
- Only `config` has a health dependency condition in production compose
- No explicit Docker healthcheck blocks are defined for individual services
