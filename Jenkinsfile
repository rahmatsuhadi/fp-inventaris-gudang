pipeline {
    agent any

    tools {
        'hudson.plugins.sonar.SonarRunnerInstallation' 'SonarScanner'
    }
    
    environment {
        SONAR_TOKEN  = credentials('SONAR_TOKEN')
        SECRET_KEY = credentials('SECRET_KEY')
        DATABASE_URL = credentials('DATABASE_URL')
        DEBUG = '1'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rahmatsuhadi/fp-inventaris-gudang.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Menginstall dependensi Python...'
                bat '''
                python -m pip install --upgrade pip
                python -m pip install --only-binary=:all: -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Menjalankan unit tests...'
                bat '''
                python manage.py test
                if exist db.sqlite3 (
                    del db.sqlite3
                )
                '''
            }
        }
        
        stage('SonarQube analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'  // nama tool di Jenkins
                    withSonarQubeEnv('SonarQube') {       // nama server di Jenkins
                        bat "\"${scannerHome}\\bin\\sonar-scanner.bat\""
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Build image aplikasi Django...'
                bat 'docker build -t inventory-app:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploy ke Docker container...'
                bat '''
                docker stop inventory-app-container || echo "Container tidak ditemukan, lanjut..."
                docker rm inventory-app-container || echo "Container tidak ada untuk dihapus."
                docker run -d --name inventory-app-container ^
                    -e SECRET_KEY=%SECRET_KEY% ^
                    -e DATABASE_URL=%DATABASE_URL% ^
                    -e DEBUG=%DEBUG% ^
                    -p 8000:8000 ^
                    -p 9100:9100 ^
                    inventory-app:latest
                '''
            }
        }
    }
}
