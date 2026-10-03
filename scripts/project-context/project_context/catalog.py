"""Catalog of indicators: which declared packages mean what. Data only; extend by adding rows.

Each table maps a package name (exact, or prefix for keys ending in '*') to (area, label).
A declared package shows that it is declared, not that it is used.
"""
from __future__ import annotations

# area values: Frontend, API, Testing, Database, Observability, Security, Technology Stack, Coding Conventions
NODE = {
    "react": ("Frontend", "React"), "next": ("Frontend", "Next.js"), "vue": ("Frontend", "Vue"),
    "@angular/core": ("Frontend", "Angular"), "svelte": ("Frontend", "Svelte"), "solid-js": ("Frontend", "Solid"),
    "react-router-dom": ("Frontend", "React Router"), "@tanstack/react-query": ("Frontend", "TanStack Query"),
    "redux": ("Frontend", "Redux"), "@reduxjs/toolkit": ("Frontend", "Redux Toolkit"), "zustand": ("Frontend", "Zustand"),
    "tailwindcss": ("Frontend", "Tailwind CSS"),
    "express": ("API", "Express"), "fastify": ("API", "Fastify"), "koa": ("API", "Koa"), "@nestjs/core": ("API", "NestJS"),
    "hono": ("API", "Hono"), "graphql": ("API", "GraphQL"), "@apollo/server": ("API", "Apollo Server"),
    "jest": ("Testing", "Jest"), "vitest": ("Testing", "Vitest"), "mocha": ("Testing", "Mocha"),
    "@playwright/test": ("Testing", "Playwright"), "cypress": ("Testing", "Cypress"), "karma": ("Testing", "Karma"),
    "@testing-library/react": ("Testing", "Testing Library"), "supertest": ("Testing", "Supertest"),
    "pg": ("Database", "PostgreSQL client (pg)"), "mysql2": ("Database", "MySQL client (mysql2)"),
    "mysql": ("Database", "MySQL client (mysql)"), "mongodb": ("Database", "MongoDB driver"),
    "mongoose": ("Database", "Mongoose"), "sequelize": ("Database", "Sequelize"), "typeorm": ("Database", "TypeORM"),
    "prisma": ("Database", "Prisma"), "@prisma/client": ("Database", "Prisma Client"), "knex": ("Database", "Knex"),
    "drizzle-orm": ("Database", "Drizzle ORM"), "redis": ("Database", "Redis client"), "ioredis": ("Database", "Redis client (ioredis)"),
    "better-sqlite3": ("Database", "SQLite (better-sqlite3)"), "sqlite3": ("Database", "SQLite (sqlite3)"),
    "winston": ("Observability", "winston (logging)"), "pino": ("Observability", "pino (logging)"),
    "bunyan": ("Observability", "bunyan (logging)"), "prom-client": ("Observability", "prom-client (metrics)"),
    "@sentry/*": ("Observability", "Sentry"), "dd-trace": ("Observability", "Datadog tracing"),
    "@opentelemetry/*": ("Observability", "OpenTelemetry"), "applicationinsights": ("Observability", "Application Insights"),
    "passport": ("Security", "Passport (authentication)"), "jsonwebtoken": ("Security", "jsonwebtoken"),
    "helmet": ("Security", "helmet (security headers)"), "next-auth": ("Security", "NextAuth"),
    "oidc-client-ts": ("Security", "oidc-client-ts"), "@auth0/*": ("Security", "Auth0 SDK"),
    "typescript": ("Technology Stack", "TypeScript"), "vite": ("Technology Stack", "Vite"), "webpack": ("Technology Stack", "webpack"),
    "esbuild": ("Technology Stack", "esbuild"), "turbo": ("Technology Stack", "Turborepo"), "nx": ("Technology Stack", "Nx"),
    "eslint": ("Coding Conventions", "ESLint"), "prettier": ("Coding Conventions", "Prettier"),
    "@biomejs/biome": ("Coding Conventions", "Biome"), "stylelint": ("Coding Conventions", "Stylelint"),
}

DOTNET = {
    "Microsoft.EntityFrameworkCore": ("Database", "Entity Framework Core"),
    "Microsoft.EntityFrameworkCore.SqlServer": ("Database", "EF Core SQL Server provider"),
    "Microsoft.EntityFrameworkCore.Sqlite": ("Database", "EF Core SQLite provider"),
    "Npgsql*": ("Database", "Npgsql (PostgreSQL provider)"),
    "Pomelo.EntityFrameworkCore.MySql": ("Database", "EF Core MySQL provider (Pomelo)"),
    "MySql.EntityFrameworkCore": ("Database", "EF Core MySQL provider"), "MySqlConnector": ("Database", "MySqlConnector"),
    "Oracle.*": ("Database", "Oracle data provider"), "Dapper": ("Database", "Dapper"),
    "MongoDB.Driver": ("Database", "MongoDB driver"), "StackExchange.Redis": ("Database", "Redis client (StackExchange.Redis)"),
    "xunit*": ("Testing", "xUnit"), "NUnit*": ("Testing", "NUnit"), "MSTest*": ("Testing", "MSTest"),
    "Microsoft.NET.Test.Sdk": ("Testing", ".NET test SDK"), "Moq": ("Testing", "Moq"), "NSubstitute": ("Testing", "NSubstitute"),
    "FluentAssertions": ("Testing", "FluentAssertions"), "coverlet*": ("Testing", "coverlet (coverage)"),
    "Testcontainers*": ("Testing", "Testcontainers"), "Microsoft.AspNetCore.Mvc.Testing": ("Testing", "ASP.NET Core integration testing"),
    "Swashbuckle*": ("API", "Swashbuckle (OpenAPI)"), "NSwag*": ("API", "NSwag (OpenAPI)"),
    "Microsoft.AspNetCore.OpenApi": ("API", "ASP.NET Core OpenAPI"), "Asp.Versioning*": ("API", "API versioning"),
    "Grpc.*": ("API", "gRPC"), "HotChocolate*": ("API", "GraphQL (HotChocolate)"),
    "OpenTelemetry*": ("Observability", "OpenTelemetry"), "Serilog*": ("Observability", "Serilog (logging)"),
    "NLog*": ("Observability", "NLog (logging)"), "Microsoft.ApplicationInsights*": ("Observability", "Application Insights"),
    "prometheus-net*": ("Observability", "prometheus-net (metrics)"),
    "Microsoft.AspNetCore.Authentication.JwtBearer": ("Security", "JWT bearer authentication"),
    "Microsoft.Identity.Web*": ("Security", "Microsoft Identity Web"), "Duende.*": ("Security", "Duende IdentityServer"),
    "MediatR*": ("Technology Stack", "MediatR"), "FluentValidation*": ("Technology Stack", "FluentValidation"),
    "AutoMapper*": ("Technology Stack", "AutoMapper"), "Mapster*": ("Technology Stack", "Mapster"),
    "StyleCop.Analyzers": ("Coding Conventions", "StyleCop analyzers"),
}

PYTHON = {
    "django": ("API", "Django"), "flask": ("API", "Flask"), "fastapi": ("API", "FastAPI"), "starlette": ("API", "Starlette"),
    "pytest": ("Testing", "pytest"), "pytest-cov": ("Testing", "pytest-cov (coverage)"), "unittest2": ("Testing", "unittest2"),
    "tox": ("Testing", "tox"), "nox": ("Testing", "nox"), "hypothesis": ("Testing", "Hypothesis"),
    "sqlalchemy": ("Database", "SQLAlchemy"), "alembic": ("Database", "Alembic (migrations)"),
    "psycopg2": ("Database", "PostgreSQL client (psycopg2)"), "psycopg2-binary": ("Database", "PostgreSQL client (psycopg2)"),
    "psycopg": ("Database", "PostgreSQL client (psycopg)"), "asyncpg": ("Database", "PostgreSQL client (asyncpg)"),
    "pymysql": ("Database", "MySQL client (PyMySQL)"), "mysqlclient": ("Database", "MySQL client (mysqlclient)"),
    "pymongo": ("Database", "MongoDB driver (pymongo)"), "redis": ("Database", "Redis client"),
    "structlog": ("Observability", "structlog (logging)"), "prometheus-client": ("Observability", "prometheus_client (metrics)"),
    "sentry-sdk": ("Observability", "Sentry"), "opentelemetry-*": ("Observability", "OpenTelemetry"),
    "authlib": ("Security", "Authlib"), "python-jose": ("Security", "python-jose (JWT)"), "pyjwt": ("Security", "PyJWT"),
    "ruff": ("Coding Conventions", "Ruff"), "black": ("Coding Conventions", "Black"), "flake8": ("Coding Conventions", "flake8"),
    "pylint": ("Coding Conventions", "Pylint"), "mypy": ("Coding Conventions", "mypy"), "isort": ("Coding Conventions", "isort"),
}

# Java: matched against "groupId:artifactId" or an artifactId / plugin id substring.
JAVA = {
    "spring-boot-starter-web": ("API", "Spring Web"), "spring-boot-starter-webflux": ("API", "Spring WebFlux"),
    "spring-boot-starter": ("Technology Stack", "Spring Boot"), "quarkus": ("Technology Stack", "Quarkus"),
    "micronaut": ("Technology Stack", "Micronaut"), "jakarta.ws.rs": ("API", "JAX-RS"),
    "spring-boot-starter-data-jpa": ("Database", "Spring Data JPA"), "hibernate-core": ("Database", "Hibernate"),
    "flyway": ("Database", "Flyway (migrations)"), "liquibase": ("Database", "Liquibase (migrations)"),
    "postgresql": ("Database", "PostgreSQL JDBC driver"), "mysql-connector": ("Database", "MySQL JDBC driver"),
    "mariadb-java-client": ("Database", "MariaDB JDBC driver"), "ojdbc": ("Database", "Oracle JDBC driver"),
    "mssql-jdbc": ("Database", "SQL Server JDBC driver"), "h2": ("Database", "H2"),
    "junit": ("Testing", "JUnit"), "mockito": ("Testing", "Mockito"), "testcontainers": ("Testing", "Testcontainers"),
    "jacoco": ("Testing", "JaCoCo (coverage)"), "spring-boot-starter-test": ("Testing", "Spring Boot Test"),
    "spring-boot-starter-security": ("Security", "Spring Security"), "spring-security": ("Security", "Spring Security"),
    "micrometer": ("Observability", "Micrometer (metrics)"), "logback": ("Observability", "Logback (logging)"),
    "log4j": ("Observability", "Log4j (logging)"), "opentelemetry": ("Observability", "OpenTelemetry"),
    "spring-boot-starter-actuator": ("Observability", "Spring Boot Actuator"),
    "checkstyle": ("Coding Conventions", "Checkstyle"), "spotless": ("Coding Conventions", "Spotless"),
}

# Database engine hints: substring (lowercase) of a declared library/image -> engine label.
ENGINES = [
    ("npgsql", "PostgreSQL"), ("postgres", "PostgreSQL"), ("psycopg", "PostgreSQL"), ("asyncpg", "PostgreSQL"),
    ("mysql", "MySQL"), ("pomelo", "MySQL"), ("mariadb", "MariaDB"), ("sqlserver", "SQL Server"), ("mssql", "SQL Server"),
    ("entityframeworkcore.sqlserver", "SQL Server"), ("oracle", "Oracle"), ("ojdbc", "Oracle"),
    ("mongo", "MongoDB"), ("sqlite", "SQLite"), ("redis", "Redis"),
]
# Connection-URL / JDBC scheme -> engine.
SCHEMES = {
    "postgres": "PostgreSQL", "postgresql": "PostgreSQL", "mysql": "MySQL", "mariadb": "MariaDB", "sqlserver": "SQL Server",
    "mongodb": "MongoDB", "redis": "Redis", "oracle": "Oracle",
}
DB_IMAGES = {
    "postgres": "PostgreSQL", "mysql": "MySQL", "mariadb": "MariaDB", "mongo": "MongoDB", "redis": "Redis",
    "mssql": "SQL Server", "sqlserver": "SQL Server", "oracle": "Oracle", "rabbitmq": "RabbitMQ", "kafka": "Kafka",
    "elasticsearch": "Elasticsearch", "memcached": "Memcached",
}

CI_FILES = {
    "Jenkinsfile": "Jenkins", ".gitlab-ci.yml": "GitLab CI", "azure-pipelines.yml": "Azure Pipelines",
    "azure-pipelines.yaml": "Azure Pipelines", ".travis.yml": "Travis CI", "appveyor.yml": "AppVeyor",
    ".drone.yml": "Drone", "bitbucket-pipelines.yml": "Bitbucket Pipelines", "cloudbuild.yaml": "Google Cloud Build",
    "buildspec.yml": "AWS CodeBuild",
}
CI_DIRS = {".circleci": "CircleCI", ".buildkite": "Buildkite"}

DEPLOY_HINTS = (
    "kubectl", "helm ", "helm upgrade", "terraform apply", "az webapp", "az containerapp", "aws deploy", "aws ecs",
    "gcloud run", "gcloud app", "serverless deploy", "flyctl deploy", "docker push", "azure/webapps-deploy",
    "azure/k8s-deploy", "aws-actions/amazon-ecs-deploy", "google-github-actions/deploy", "pulumi up",
)

SOURCE_EXTS = {
    ".py": "Python", ".cs": "C#", ".ts": "TypeScript", ".tsx": "TypeScript (JSX)", ".js": "JavaScript", ".jsx": "JavaScript (JSX)",
    ".java": "Java", ".kt": "Kotlin", ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
    ".scala": "Scala", ".cpp": "C++", ".c": "C", ".sh": "Shell", ".ps1": "PowerShell", ".sql": "SQL", ".vue": "Vue SFC",
    ".svelte": "Svelte",
}

SIDE_EFFECT = ("deploy", "publish", "release", "migrate", "seed", "reset", "drop", "push", "destroy", "apply", "prune", "clean", "install")


def match(table: dict, name: str):
    """Exact match first, then prefix rows ending in '*'. Returns (area, label) or None."""
    if name in table:
        return table[name]
    low = name.lower()
    for k, v in table.items():
        if k.endswith("*") and low.startswith(k[:-1].lower()):
            return v
    return None
