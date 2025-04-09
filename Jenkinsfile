pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/chiku153x/pipeline-tester.git'
        DOCKER_IMAGE = "pipeline-tester"
        BUILD_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Setup') {
            steps {
                cleanWs() // Cleans the workspace to avoid "not in a git directory" errors
                checkout scm // Uses Multibranch Pipeline's default SCM configuration
                sh 'git status'
            }
        }

        stage('Unittest & Coverage') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python --version
                    pip install -U pip
                    pip --version
                    pip install -r requirements.txt || true
                    pip install coverage
                    coverage run -m pytest
                    coverage xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    script {
                        def scannerHome = tool 'sonar-scanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=pipeline-tester \
                                -Dsonar.projectName='Pipeline Tester' \
                                -Dsonar.sources=. \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.sourceEncoding=UTF-8
                        """
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_TAG} ."
                }
            }
        }

        stage('Tag & Push Git') {
            steps {
                script {
                    sh """
                        git config user.name "Jenkins"
                        git config user.email "jenkins@example.com"
                        git tag -a v${BUILD_TAG} -m "Build #${BUILD_TAG}"
                        # git push origin v${BUILD_TAG}
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "Docker tag and push logic goes here"
                    // Example:
                    // docker tag ${DOCKER_IMAGE}:${BUILD_TAG} your-registry/${DOCKER_IMAGE}:${BUILD_TAG}
                    // docker push your-registry/${DOCKER_IMAGE}:${BUILD_TAG}
                }
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline execution completed.'
        }
        failure {
            echo '❌ Pipeline failed.e'
        }
    }
}
