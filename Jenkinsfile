pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/chiku153x/pipeline-tester.git'
        DOCKER_IMAGE = 'your-artifactory-domain.com/your-repo/pipeline-tester'
        BUILD_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Setup') {
            steps {
                git branch: 'master', url: "${GIT_REPO}"
            }
        }

        stage('Unittest') {
            steps {
                sh 'pip install -r requirements.txt || true' // Optional, if you have a requirements.txt
                sh 'pip install pytest'
                sh 'pytest'
            }
        }

        stage('Code Analysis') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
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
                        git push origin v${BUILD_TAG}
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://your-artifactory-domain.com', 'artifactory-credentials-id') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
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
