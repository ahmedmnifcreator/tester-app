## Config management
PiggyMetrics centralizes configuration via Spring Cloud Config.

## Config server
- Located in `config/`
- Exposes configuration over HTTP on port `8888` in development compose
- Serves application properties from `src/main/resources`
- Uses `bootstrap.yml` in each service to locate config server

## Shared configuration
- `config/src/main/resources/shared/application.yml` contains common settings for all services
- Common properties include:
  - `spring.application.name`
  - `server.port`
  - `eureka.client.service-url.defaultZone`
  - `spring.cloud.config.uri`
  - security and OAuth2 URIs

## Service bootstrap
- Each service includes `bootstrap.yml` to set config server URI and `spring.application.name`
- `bootstrap.yml` may also set active profiles and property sources

## Local development
- Docker Compose dev uses `spring.cloud.config.uri=http://config:8888`
- Services request config from `config` container at startup

## Configuration pattern
- Service-specific `bootstrap.yml` references config server and Eureka
- Shared `application.yml` from config service centralizes cross-service settings
- Override local ports in `docker-compose.dev.yml`

## Secrets and environment variables
- Secrets are passed via Docker environment variables and `COMPONENT_PASSWORD` values
- Sensitive credentials are not stored in source control

## Configuration flow
1. Service starts and loads `bootstrap.yml`
2. It connects to Config Server URI
3. Config Server returns properties from shared and service-specific files
4. Service registers with Eureka
5. Service starts with resolved configuration

## Profiles
- No explicit Spring profiles are defined in the repository
- Development vs production is controlled by different Docker compose files and environment variable injection
