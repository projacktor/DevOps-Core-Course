FROM maven:3.9.6-eclipse-temurin-17 AS builder

WORKDIR /build

COPY pom.xml .
RUN mvn -B dependency:go-offline

COPY src ./src
RUN mvn -B package -DskipTests


FROM gcr.io/distroless/java17-debian12

WORKDIR /app

COPY --from=builder /build/target/info-service-1.0.0.jar ./app.jar

EXPOSE 8000
USER nonroot

ENTRYPOINT ["java", "-jar", "app.jar"]