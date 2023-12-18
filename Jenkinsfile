pipeline {
    agent any

    environment {
        AZURE_TENANT_ID = '<your-azure-tenant-id>'
        AZURE_CLIENT_ID = '<your-azure-client-id>'
        AZURE_CLIENT_SECRET = '<your-azure-client-secret>'
    }

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
