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
                git branch: 'master', url: "${GIT_REPO}"
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
                    pip install -r requirements.txt || true  # Optional, if you have a requirements.txt
                    pip install coverage
                    coverage run -m pytest
                    coverage xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {  // Match Jenkins > Configure System
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
                    dockerImage = docker.build("${DOCKER_IMAGE}:${BUILD_TAG}")
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
                    // Uncomment and configure this for Artifactory push
                    // docker.withRegistry('https://your-artifactory-domain.com', 'artifactory-credentials-id') {
                    //     dockerImage.push()
                    //     dockerImage.push('latest')
                    // }
                    echo "Docker tag and push required"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
