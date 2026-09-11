pipeline {

    agent any

    environment {
    PYTHON = 'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    DOCKER = 'C:\\Users\\user\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
 }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '"%PYTHON%" --version'
            }
        }
        stage('Check Docker') {
    steps {
        bat '"%DOCKER%" --version'
    }
}
        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m unittest discover -s tests -v'
            }
        }

    }

    post {

        success {
            echo '✅ CI Pipeline completed successfully!'
        }

        failure {
            echo '❌ CI Pipeline failed!'
        }

    }
}
