## config
- Name: config
- Purpose: Spring Cloud Config Server
- Responsibilities: serve config from classpath shared directory; authenticate via basic auth; provide bootstrap configuration.
- Internal architecture: `ConfigApplication`, `SecurityConfig`
- Dependencies: Spring Cloud Config Server, Spring Security
- Consumed services: none
- Exposed services: config HTTP endpoint on 8888
- Main packages: `com.piggymetrics.config`
- Important classes: `ConfigApplication`, `SecurityConfig`
- Startup order: first

## registry
- Name: registry
- Purpose: Eureka service registry
- Responsibilities: service discovery and registration, Eureka UI
- Internal architecture: `RegistryApplication`
- Dependencies: Spring Cloud Netflix Eureka Server
- Consumed services: config server
- Exposed services: Eureka on 8761
- Main packages: `com.piggymetrics.registry`
- Important classes: `RegistryApplication`
- Startup order: after config

## gateway
- Name: gateway
- Purpose: API gateway using Zuul
- Responsibilities: route requests to backend services, use service discovery
- Internal architecture: `GatewayApplication`
- Dependencies: Spring Cloud Netflix Zuul, Eureka client
- Consumed services: registry, config server
- Exposed services: gateway proxy at port 80 in production
- Main packages: `com.piggymetrics.gateway`
- Important classes: `GatewayApplication`
- Startup order: after config

## auth-service
- Name: auth-service
- Purpose: OAuth2 authorization server and user management
- Responsibilities: authenticate users, issue tokens, validate user info, store users
- Internal architecture: `AuthApplication`, `WebSecurityConfig`, `OAuth2AuthorizationConfig`, `UserController`, `UserServiceImpl`, `MongoUserDetailsService`
- Dependencies: Spring Boot Web, Spring Security, Spring Security OAuth2, Spring Data MongoDB, Eureka client, Config client, Sleuth
- Consumed services: config server
- Exposed services: `/uaa/users`, OAuth2 endpoints, user-info endpoint
- Main packages: `com.piggymetrics.auth`, `com.piggymetrics.auth.config`, `com.piggymetrics.auth.controller`, `com.piggymetrics.auth.domain`, `com.piggymetrics.auth.repository`, `com.piggymetrics.auth.service`
- Important classes: `AuthApplication`, `WebSecurityConfig`, `OAuth2AuthorizationConfig`, `UserController`, `UserServiceImpl`, `MongoUserDetailsService`
- Startup order: after config

## account-service
- Name: account-service
- Purpose: manage account domain and trigger statistics updates
- Responsibilities: create accounts, retrieve current account, save account updates, call auth service and statistics service
- Internal architecture: `AccountApplication`, `ResourceServerConfig`, `AccountController`, `AccountServiceImpl`, `AccountRepository`, `AuthServiceClient`, `StatisticsServiceClient`
- Dependencies: Spring Boot Web, Spring Data MongoDB, Spring Cloud OpenFeign, Eureka client, Hystrix, Config client, Sleuth
- Consumed services: auth-service, statistics-service, config server, registry
- Exposed services: `/accounts`
- Main packages: `com.piggymetrics.account`, `com.piggymetrics.account.controller`, `com.piggymetrics.account.service`, `com.piggymetrics.account.repository`, `com.piggymetrics.account.client`
- Important classes: `AccountApplication`, `ResourceServerConfig`, `AccountController`, `AccountServiceImpl`, `AuthServiceClient`, `StatisticsServiceClient`
- Startup order: after config

## statistics-service
- Name: statistics-service
- Purpose: calculate and store financial statistics
- Responsibilities: normalize incomes and expenses, compute statistics, persist daily data points, use exchange rates API
- Internal architecture: `StatisticsApplication`, `ResourceServerConfig`, `StatisticsController`, `StatisticsServiceImpl`, `DataPointRepository`, `ExchangeRatesClient`
- Dependencies: Spring Boot Web, Spring Data MongoDB, Spring Cloud OpenFeign, Eureka client, Hystrix stream, Config client, Sleuth
- Consumed services: external rates API, config server, registry
- Exposed services: `/statistics`
- Main packages: `com.piggymetrics.statistics`, `com.piggymetrics.statistics.controller`, `com.piggymetrics.statistics.service`, `com.piggymetrics.statistics.repository`, `com.piggymetrics.statistics.domain`
- Important classes: `StatisticsApplication`, `ResourceServerConfig`, `StatisticsController`, `StatisticsServiceImpl`, `ExchangeRatesClient`, `DataPointRepository`
- Startup order: after config

## notification-service
- Name: notification-service
- Purpose: manage notification settings and send scheduled notifications
- Responsibilities: store recipient settings, expose current account notification settings, send backup and remind emails using schedule
- Internal architecture: `NotificationServiceApplication`, `ResourceServerConfig`, `RecipientController`, `RecipientServiceImpl`, `NotificationServiceImpl`, `EmailServiceImpl`, `AccountServiceClient`
- Dependencies: Spring Boot Web, Spring Data MongoDB, Spring Cloud OpenFeign, Eureka client, Config client, Sleuth
- Consumed services: account-service, config server, registry
- Exposed services: `/recipients`
- Main packages: `com.piggymetrics.notification`, `com.piggymetrics.notification.controller`, `com.piggymetrics.notification.service`, `com.piggymetrics.notification.repository`, `com.piggymetrics.notification.domain`, `com.piggymetrics.notification.client`
- Important classes: `NotificationServiceApplication`, `ResourceServerConfig`, `RecipientController`, `RecipientServiceImpl`, `NotificationServiceImpl`, `EmailServiceImpl`
- Startup order: after config

## monitoring
- Name: monitoring
- Purpose: Hystrix dashboard
- Responsibilities: expose Hystrix dashboard UI
- Internal architecture: `MonitoringApplication`
- Dependencies: Spring Cloud Netflix Hystrix Dashboard, Config client, Eureka client
- Consumed services: config server
- Exposed services: dashboard on 9000
- Main packages: `com.piggymetrics.monitoring`
- Important classes: `MonitoringApplication`
- Startup order: after config

## turbine-stream-service
- Name: turbine-stream-service
- Purpose: aggregate Hystrix metrics streams
- Responsibilities: expose Turbine stream endpoint
- Internal architecture: `TurbineStreamServiceApplication`
- Dependencies: Spring Cloud Netflix Eureka client, Config client
- Consumed services: config server
- Exposed services: Turbine stream on 8989
- Main packages: `com.piggymetrics.turbine`
- Important classes: `TurbineStreamServiceApplication`
- Startup order: after config
