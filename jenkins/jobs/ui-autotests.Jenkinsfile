pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        booleanParam(name: 'USE_LOCAL_REPO', defaultValue: true, description: 'Use local repository mounted into Jenkins instead of cloning from GitHub')
        string(name: 'LOCAL_REPO_PATH', defaultValue: '/local-repo', description: 'Mounted local repository path inside Jenkins container')
        string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/julsel-web/Selenium_test_otus.git', description: 'GitHub repository with autotests')
        string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to checkout')
        booleanParam(name: 'START_TEST_STACK', defaultValue: true, description: 'Start OpenCart + Selenoid docker-compose stack before tests')
        booleanParam(name: 'TEARDOWN_TEST_STACK', defaultValue: false, description: 'Stop docker-compose stack after build')
        string(name: 'STACK_COMPOSE_FILE', defaultValue: '/opt/jenkins-stack/opencart-stack/docker-compose.yml', description: 'Path to docker-compose file with OpenCart and Selenoid')
        string(name: 'SELENOID_URL', defaultValue: 'http://host.docker.internal:4445/wd/hub', description: 'Remote WebDriver / Selenoid URL')
        string(name: 'APP_URL', defaultValue: 'http://host.docker.internal:8082', description: 'Application base URL')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser name')
        string(name: 'BROWSER_VERSION', defaultValue: '120.0', description: 'Browser version for Selenoid')
        string(name: 'THREADS', defaultValue: '1', description: 'Parallel test threads for pytest-xdist')
    }

    environment {
        VENV_DIR = "${WORKSPACE}/.venv"
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Configure parameters') {
            steps {
                script {
                    properties([
                        parameters([
                            booleanParam(name: 'USE_LOCAL_REPO', defaultValue: true, description: 'Use local repository mounted into Jenkins instead of cloning from GitHub'),
                            string(name: 'LOCAL_REPO_PATH', defaultValue: '/local-repo', description: 'Mounted local repository path inside Jenkins container'),
                            string(name: 'GIT_REPO_URL', defaultValue: 'https://github.com/julsel-web/Selenium_test_otus.git', description: 'GitHub repository with autotests'),
                            string(name: 'GIT_BRANCH', defaultValue: 'main', description: 'Git branch to checkout'),
                            booleanParam(name: 'START_TEST_STACK', defaultValue: true, description: 'Start OpenCart + Selenoid docker-compose stack before tests'),
                            booleanParam(name: 'TEARDOWN_TEST_STACK', defaultValue: false, description: 'Stop docker-compose stack after build'),
                            string(name: 'STACK_COMPOSE_FILE', defaultValue: '/opt/jenkins-stack/opencart-stack/docker-compose.yml', description: 'Path to docker-compose file with OpenCart and Selenoid'),
                            string(name: 'SELENOID_URL', defaultValue: 'http://host.docker.internal:4445/wd/hub', description: 'Remote WebDriver / Selenoid URL'),
                            string(name: 'APP_URL', defaultValue: 'http://host.docker.internal:8082', description: 'Application base URL'),
                            choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser name'),
                            string(name: 'BROWSER_VERSION', defaultValue: '120.0', description: 'Browser version for Selenoid'),
                            string(name: 'THREADS', defaultValue: '1', description: 'Parallel test threads for pytest-xdist')
                        ])
                    ])
                }
            }
        }

        stage('Load tests') {
            steps {
                script {
                    deleteDir()
                    if (params.USE_LOCAL_REPO) {
                        sh '''
                            test -d "${LOCAL_REPO_PATH}"
                            cp -a "${LOCAL_REPO_PATH}/." "${WORKSPACE}/"
                            rm -rf "${WORKSPACE}/jenkins_home"
                        '''
                    } else {
                        git branch: params.GIT_BRANCH, url: params.GIT_REPO_URL
                    }
                }
            }
        }

        stage('Start test stack') {
            when {
                expression { return params.START_TEST_STACK }
            }
            steps {
                sh '''
                    mkdir -p /opt/jenkins-stack/opencart-stack/videos
                    docker-compose -f "${STACK_COMPOSE_FILE}" up -d
                '''
            }
        }

        stage('Wait for services') {
            when {
                expression { return params.START_TEST_STACK }
            }
            steps {
                sh '''
                    python3 - <<'PY'
import sys
import time
import urllib.request
import urllib.error

checks = [
    ("OpenCart", "${APP_URL}"),
    ("Selenoid", "${SELENOID_URL}".replace("/wd/hub", "/status")),
]

for title, url in checks:
    last_error = None
    for _ in range(60):
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if 200 <= response.status < 400:
                    print(f"{title} is ready: {url}")
                    break
                last_error = f"HTTP {response.status}"
        except urllib.error.HTTPError as exc:
            if 200 <= exc.code < 400:
                print(f"{title} is ready: {url}")
                break
            last_error = f"HTTP {exc.code}"
        except Exception as exc:
            last_error = str(exc)
        time.sleep(5)
    else:
        print(f"{title} is not ready: {url} ({last_error})", file=sys.stderr)
        sys.exit(1)
PY
                '''
            }
        }

        stage('Prepare environment') {
            steps {
                sh '''
                    python3 -m venv "${VENV_DIR}"
                    . "${VENV_DIR}/bin/activate"
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        . "${VENV_DIR}/bin/activate"
                        rm -rf allure-results allure-report
                        pytest -v \
                            -n "${THREADS}" \
                            --headless \
                            --remote \
                            --browser "${BROWSER}" \
                            --browser-version "${BROWSER_VERSION}" \
                            --base-url "${APP_URL}" \
                            --remote-url "${SELENOID_URL}" \
                            --alluredir allure-results
                    '''
                }
            }
        }

        stage('Build Allure HTML') {
            steps {
                sh '''
                    if [ -d allure-results ]; then
                      allure generate allure-results --clean -o allure-report
                    fi
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**, allure-report/**, screenshots/**', allowEmptyArchive: true
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure Report'
            ])
        }
        cleanup {
            script {
                if (params.START_TEST_STACK && params.TEARDOWN_TEST_STACK) {
                    sh '''
                        if [ -f "${STACK_COMPOSE_FILE}" ]; then
                          docker-compose -f "${STACK_COMPOSE_FILE}" down -v || true
                        fi
                    '''
                }
            }
        }
    }
}
