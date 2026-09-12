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

        stage('Check Minikube') {
            steps {
                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" profile list'
                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" status'
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

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER%" build -t devops-task-app:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" image load devops-task-app:%BUILD_NUMBER%'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- set image deployment/devops-task-app devops-task-app=devops-task-app:%BUILD_NUMBER%'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- set resources deployment/devops-task-app -c devops-task-app --requests=cpu=100m,memory=128Mi --limits=cpu=500m,memory=512Mi'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- apply -f k8s/service.yaml'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- rollout status deployment/devops-task-app --timeout=120s'
            }
        }

        stage('Verify Deployment') {
            steps {

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- get deployment devops-task-app'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- get pods'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- get service devops-task-app'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- get pods -o wide'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- get deployment devops-task-app -o jsonpath="{.spec.template.spec.containers[0].image}"'
            }
        }

        stage('Application Health Check') {
            steps {
                bat '''"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- exec deployment/devops-task-app -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').status)"'''
            }
        }
        stage('Resource Check') {
            steps {
                bat '''
                powershell -NoProfile -ExecutionPolicy Bypass -Command "$maxAttempts=6; $attempt=1; while ($attempt -le $maxAttempts) { Write-Host ('Checking Kubernetes metrics - Attempt ' + $attempt + '/' + $maxAttempts); & 'C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe' kubectl -- top pods; if ($LASTEXITCODE -eq 0) { exit 0 }; Start-Sleep -Seconds 10; $attempt++ }; Write-Host 'Metrics are still unavailable after waiting.'; exit 1"
                '''

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- top nodes'

                bat '"C:\\Program Files\\Kubernetes\\Minikube\\minikube.exe" kubectl -- describe deployment devops-task-app'
            }
        }
    }

    post {

        success {
            echo '✅ CI/CD Pipeline completed successfully!'
        }

        failure {
            echo '❌ CI/CD Pipeline failed!'
        }
    }
}
