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
        
        PORT_CLIENT_ID = credentials('port-client-id')
        PORT_CLIENT_SECRET = credentials('port-client-secret')
        
        ACCESS_TOKEN = ""
        endpoint_url = ""

    }
    
    // uncomment for webhook trigger
    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'storage_name', value: '$.payload.properties.storage_name'],
                [key: 'storage_location', value: '$.payload.properties.storage_location'],
                [key: 'RUN_ID', value: '$.context.runId'],
                [key: 'BLUEPRINT_ID', value: '$.context.blueprint']
            ],
            causeString: 'Triggered on RUN_ID',
            regexpFilterExpression: '',
            regexpFilterText: '',
            printContributedVariables: true,
            printPostContent: true
        )
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github', url: 'git@github.com:phalbert/azure-resources-terraform.git'
            }
        }
        stage('Terraform') {
            steps {

                    ansiColor('xterm') {
                    withCredentials([azureServicePrincipal(
                    credentialsId: 'azure',
                    subscriptionIdVariable: 'ARM_SUBSCRIPTION_ID',
                    clientIdVariable: 'ARM_CLIENT_ID',
                    clientSecretVariable: 'ARM_CLIENT_SECRET',
                    tenantIdVariable: 'ARM_TENANT_ID'
                )]) {
                        sh 'terraform init'
                        sh 'terraform validate'
                        sh """
                        
                        echo "Creating Terraform Plan"
                        terraform plan -out=tfplan -var storage_account_name=$storage_name -var location=$storage_location -var "client_id=$ARM_CLIENT_ID" -var "client_secret=$ARM_CLIENT_SECRET" -var "subscription_id=$ARM_SUBSCRIPTION_ID" -var "tenant_id=$ARM_TENANT_ID"
                        """
                        sh "terraform apply -auto-approve -input=false tfplan"
                        }
                }
            }
        }
        stage('Get access token') {
            steps {
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
                    ACCESS_TOKEN = payloadJson.accessToken
                }
            }
        }

		stage('Create entity') {
            steps {
                script {
                    def terraformOutput = sh(script: 'terraform output endpoint_url | sed \'s/"//g\'', returnStdout: true)
                    endpoint_url = terraformOutput
                
                    def status_report_response = sh(script: """
						curl --location --request POST "https://api.getport.io/v1/blueprints/$BLUEPRINT_ID/entities?upsert=true&run_id=$RUN_ID&create_missing_related_entities=true" \
        --header "Authorization: Bearer $ACCESS_TOKEN" \
        --header "Content-Type: application/json" \
        --data-raw '{
				"identifier": "$storage_name",
				"title": "$storage_name",
				"properties": {"storage_name":"$storage_name","storage_location":"$storage_location", "endpoint": "$endpoint_url"},
				"relations": {}
			}'

                    """, returnStdout: true)

                    println(status_report_response)
                }
            }
        }

        stage('Send logs example') {
            steps {
                script {
                    def logs_report_response = sh(script: """
                        curl -X POST \
                            -H "Content-Type: application/json" \
                            -H "Authorization: Bearer ${ACCESS_TOKEN}" \
                            -d '{"message": "this is a log test message example"}' \
                            "https://api.getport.io/v1/actions/runs/$RUN_ID/logs"
                    """, returnStdout: true)

                    println(logs_report_response)
                }
            }
        }

        stage('Update status example') {
            steps {
                script {
                    def status_report_response = sh(script: """
                        curl -X PATCH \
                          -H "Content-Type: application/json" \
                          -H "Authorization: Bearer ${ACCESS_TOKEN}" \
                          -d '{"status":"SUCCESS", "message": {"run_status": "Jenkins CI/CD Run completed successfully!"}}' \
                             "https://api.getport.io/v1/actions/runs/${RUN_ID}"
                    """, returnStdout: true)

                    println(status_report_response)
                }
            }
        }
    }
}
