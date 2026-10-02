## Overall architecture
PiggyMetrics is a Spring Cloud microservice application with a centralized configuration server, Eureka service registry, API gateway, multiple backend services, RabbitMQ messaging, and MongoDB persistence.

## Architecture style
- Microservice architecture
- Service-oriented distributed system
- API gateway/edge service with Zuul
- Client-side service discovery via Eureka
- OAuth2 resource servers for authentication and authorization
- Centralized configuration with Spring Cloud Config

## Microservice architecture
- `config` provides centralized configuration.
- `registry` provides Eureka service discovery.
- `gateway` is a Zuul-based edge proxy.
- `auth-service` is the OAuth2 authorization and user management server.
- `account-service` manages account data and triggers statistics updates.
- `statistics-service` calculates and persists normalized financial statistics.
- `notification-service` manages recipient settings and sends scheduled emails.
- `monitoring` hosts the Hystrix dashboard.
- `turbine-stream-service` aggregates Hystrix metrics streams.

## Main components
- `config`: Config server, security config, native profile settings.
- `registry`: Eureka server.
- `gateway`: API gateway with discovery.
- `auth-service`: authorization server, user store, token endpoint.
- `account-service`: account lifecycle, persistence, statistics integration.
- `statistics-service`: statistics calculations, exchange rate conversion, data points.
- `notification-service`: notification settings, recipient persistence, scheduled email sending.
- `monitoring`: Hystrix dashboard.
- `turbine-stream-service`: Turbine metrics aggregation.

## Component responsibilities
- `config` serves shared YAML configuration and authenticates config clients.
- `registry` registers and discovers services.
- `gateway` routes incoming traffic through Zuul.
- `auth-service` validates user credentials, issues tokens, and exposes user info.
- `account-service` stores account documents and calls `statistics-service` on updates.
- `statistics-service` computes statistics and stores time series datapoints.
- `notification-service` stores recipient settings and sends notifications.
- `monitoring` exposes Hystrix dashboard UI.
- `turbine-stream-service` exposes Turbine stream endpoint.

## Technology stack
- Java 8
- Spring Boot 2.0.3.RELEASE
- Spring Cloud Finchley.RELEASE
- Spring Cloud Config
- Spring Cloud Netflix Eureka, Zuul, Hystrix, Hystrix Dashboard
- Spring Cloud OpenFeign
- Spring Security OAuth2
- Spring Data MongoDB
- RabbitMQ
- MongoDB
- Maven
- Docker / Docker Compose

## Communication style
- HTTP REST APIs
- Feign declarative clients for internal service calls
- Eureka for service discovery
- OAuth2 token-based authorization
- Centralized config via Config server
- Scheduled tasks in notification-service
- Hystrix and Turbine metrics over RabbitMQ

## External services
- RabbitMQ as message broker
- MongoDB as persistence for domain services
- External exchange rate API configured via `rates.url`
- Email sender via Spring `JavaMailSender`

## Design patterns
- Microservices decomposition
- API gateway / proxy
- OAuth2 resource server
- Service registry/discovery
- Declarative REST client (Feign)
- Circuit breaker / fallback
- Centralized configuration server
- Repository pattern with Spring Data MongoDB

## Startup sequence
1. RabbitMQ
2. Config server
3. Eureka registry
4. Gateway
5. Auth service
6. Account service
7. Statistics service
8. Notification service
9. Monitoring service
10. Turbine stream service

## Configuration flow
- Each service uses `bootstrap.yml` to locate the config server at `http://config:8888`.
- Config server uses native profile and `classpath:/shared`.
- Shared YAML files provide service-specific config and common settings.
- Environment variables supply secrets and service passwords.
