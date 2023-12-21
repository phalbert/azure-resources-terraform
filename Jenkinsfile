pipeline {
    agent any

    stages {
        stage('Init') {
            steps {
                sh 'terraform init'
            }
        }

        stage('Apply') {
            steps {
                sh 'terraform apply --auto-approve'
            }
        }
    }
}
