FROM jenkins/jenkins:lts-jdk17

USER root

ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    unzip \
    python3 \
    python3-venv \
    python3-pip \
    docker.io \
    docker-compose \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG ALLURE_VERSION=2.35.1
RUN curl -fsSL -o /tmp/allure.tgz \
    "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf /tmp/allure.tgz -C /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}/bin/allure" /usr/local/bin/allure \
    && rm -f /tmp/allure.tgz

COPY jenkins/plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

COPY jenkins/init.groovy.d /usr/share/jenkins/ref/init.groovy.d
COPY jenkins/jobs /usr/share/jenkins/ref/jobs
COPY opencart-stack /opt/jenkins-stack/opencart-stack

USER jenkins
