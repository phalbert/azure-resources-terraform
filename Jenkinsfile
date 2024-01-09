import groovy.json.JsonSlurper

pipeline {
    agent any
    tools {
        "org.jenkinsci.plugins.terraform.TerraformInstallation" "terraform"
    }
    environment {
        TF_HOME = tool('terraform')
        TF_IN_AUTOMATION = "true"
        PATH = "$TF_HOME:$PATH"
        
        PORT_ACCESS_TOKEN = ""
        endpoint_url = ""

    }
    
    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'STORAGE_NAME', value: '$.payload.properties.storage_name'],
                [key: 'STORAGE_LOCATION', value: '$.payload.properties.storage_location'],
                [key: 'PORT_RUN_ID', value: '$.context.runId'],
                [key: 'BLUEPRINT_ID', value: '$.context.blueprint']
            ],
            causeString: 'Triggered by Port',
            allowSeveralTriggersPerBuild: true,
            tokenCredentialId: "WEBHOOK_TOKEN",
            
            regexpFilterExpression: '',
            regexpFilterText: '',
            printContributedVariables: true,
            printPostContent: true
        )
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github', url: 'git@github.com:port-labs/jenkins-terraform-azure.git'
            }
        }
        stage('Get access token') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'port-credentials', 
                    usernameVariable: 'PORT_CLIENT_ID', 
                    passwordVariable: 'PORT_CLIENT_SECRET')]) {
                    script {
                        // Execute the curl command and capture the output
                        def result = sh(returnStdout: true, script: """
                            accessTokenPayload=\$(curl -X POST \
                                -H "Content-Type: application/json" \
                                -d '{"clientId": "${PORT_CLIENT_ID}", "clientSecret": "${PORT_CLIENT_SECRET}"}' \
                                -s "https://api.getport.io/v1/auth/access_token")
                            echo \$accessTokenPayload
                        """)

                        // Parse the JSON response using JsonSlurper
                        def jsonSlurper = new JsonSlurper()
                        def payloadJson = jsonSlurper.parseText(result.trim())

                        // Access the desired data from the payload
                        PORT_ACCESS_TOKEN = payloadJson.accessToken
                    }
                }
            }
        }
        
        stage('Terraform Azure') {
            steps {
                withCredentials([azureServicePrincipal(
                    credentialsId: 'azure',
                    subscriptionIdVariable: 'ARM_SUBSCRIPTION_ID',
                    clientIdVariable: 'ARM_CLIENT_ID',
                    clientSecretVariable: 'ARM_CLIENT_SECRET',
                    tenantIdVariable: 'ARM_TENANT_ID'
                ), usernamePassword(credentialsId: 'port-credentials', usernameVariable: 'TF_VAR_port_client_id', passwordVariable: 'TF_VAR_port_client_secret')]) {
                    dir('terraform') {
                        script {
                            echo 'Initializing Terraform'
                            sh 'terraform init'
                            
                            echo 'Validating Terraform configuration'
                            sh 'terraform validate'
                            
                            echo 'Creating Terraform Plan for Azure changes'
                            sh """
                            terraform plan -out=tfazure -var storage_account_name=$STORAGE_NAME -var location=$STORAGE_LOCATION -var port_run_id=$PORT_RUN_ID -target=azurerm_storage_account.storage_account
                            """
                            
                            echo 'Applying Terraform changes to Azure'
                            sh 'terraform apply -auto-approve -input=false tfazure'

                            echo 'Creating Terraform Plan for Port changes'
                            sh """
                            terraform plan -out=tfport -var storage_account_name=$STORAGE_NAME -var location=$STORAGE_LOCATION -var port_run_id=$PORT_RUN_ID
                            """
                            
                            echo 'Applying Terraform changes to Port'
                            sh 'terraform apply -auto-approve -input=false tfport'
                        }
                    }
                }
            }
        }
        stage('Notify Port') {
            steps {
                script {
                    def logs_report_response = sh(script: """
                        curl -X POST \
                            -H "Content-Type: application/json" \
                            -H "Authorization: Bearer ${PORT_ACCESS_TOKEN}" \
                            -d '{"message": "Created port entity"}' \
                            "https://api.getport.io/v1/actions/runs/$PORT_RUN_ID/logs"
                    """, returnStdout: true)

                    println(logs_report_response)
                }
            }
        }

        stage('Update Run Status') {
            steps {
                script {
                    def status_report_response = sh(script: """
                        curl -X PATCH \
                          -H "Content-Type: application/json" \
                          -H "Authorization: Bearer ${PORT_ACCESS_TOKEN}" \
                          -d '{"status":"SUCCESS", "message": {"run_status": "Jenkins CI/CD Run completed successfully!"}}' \
                             "https://api.getport.io/v1/actions/runs/${PORT_RUN_ID}"
                    """, returnStdout: true)

                    println(status_report_response)
                }
            }
        }
    }
    
    post {

        failure {
            // Update Port Run failed.
            script {
                def status_report_response = sh(script: """
                    curl -X PATCH \
                        -H "Content-Type: application/json" \
                        -H "Authorization: Bearer ${PORT_ACCESS_TOKEN}" \
                        -d '{"status":"FAILURE", "message": {"run_status": "Failed to create azure resource ${STORAGE_NAME}"}}' \
                            "https://api.getport.io/v1/actions/runs/${PORT_RUN_ID}"
                """, returnStdout: true)

                println(status_report_response)
            }
        }

        // Clean after build
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: false,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                               [pattern: '.propsfile', type: 'EXCLUDE']])
        }
    }
}