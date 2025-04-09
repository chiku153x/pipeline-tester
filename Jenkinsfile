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
                echo "Repository already checked out by multibranch pipeline"
                sh 'git status || true' // Avoid breaking build if status fails
            }
        }

        stage('Unittest & Coverage') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python --version
                    pip install -U pip
                    pip install -r requirements.txt || true
                    pip install coverage pytest
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

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_TAG} ."
                }
            }
        }

        stage('Tag Git') {
            steps {
                script {
                    sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@example.com"
                        git tag -a v${BUILD_TAG} -m "Build #${BUILD_TAG}" || echo "Tag already exists"
                        # git push origin v${BUILD_TAG}
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "Docker tag and push logic goes here"
                    // Optional: Uncomment when ready to push
                    // sh "docker tag ${DOCKER_IMAGE}:${BUILD_TAG} your-artifactory.com/${DOCKER_IMAGE}:${BUILD_TAG}"
                    // sh "docker push your-artifactory.com/${DOCKER_IMAGE}:${BUILD_TAG}"
                }
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline execution completed.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
