// Jenkinsfile

pipeline {
    agent any

    stages {

        // Tahap 1: Mengambil kode dari GitHub
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git'
            }
        }

        // Tahap 2: Menginstall dependensi
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Menginstall dependensi Python...'
                    sh 'python -m pip install -r requirements.txt'
                }
            }
        }

        // Tahap 3: Menjalankan tes
        stage('Run Tests') {
            steps {
                script {
                    echo 'Menjalankan unit tests...'
                    sh 'python manage.py test'
                }
            }
        }

        // Tahap 4: Analisis Kode dengan SonarQube
        // stage('SonarQube Analysis') {
        //     steps {
        //         withSonarQubeEnv('MySonarQube') {
        //             sh 'sonar-scanner'
        //         }
        //     }
        // }

        // Tahap 5: Membangun Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Membangun Docker image...'
                    sh 'docker build -t inventory-app:latest .'
                }
            }
        }

        // Tahap 6: Menjalankan Container (Deployment)
        stage('Deploy to Docker') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'DATABASE_URL', variable: 'DB_URL'),
                                     string(credentialsId: 'SECRET_KEY', variable: 'SEC_KEY')]) {
                        
                        echo 'Membuat file environment sementara...'
                        sh '''
                            echo DATABASE_URL=${DB_URL} > temp.env
                            echo SECRET_KEY=${SEC_KEY} >> temp.env
                            echo DEBUG=0 >> temp.env
                        '''

                        echo 'Menghentikan dan menghapus container lama (jika ada)...'
                        sh 'docker stop inventory-app-container || true && docker rm inventory-app-container || true'

                        echo 'Menjalankan container baru...'
                        sh 'docker run -d --name inventory-app-container -p 8000:8000 --env-file temp.env inventory-app:latest'
                    }
                }
            }
        }
    }
}