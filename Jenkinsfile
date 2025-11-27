pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['main', 'dev', 'qa', 'stage', 'prod'],
            description: 'Select environment pipeline to run'
        )
    }

    stages {
        stage('Testing Environment') {
            steps {
                echo 'Setting up testing environment...'

                script {
                    // Select file based on parameter
                    def fileToLoad = ""

                    if (params.ENVIRONMENT == 'main') {
                        fileToLoad = 'pipelines/Jenkinsfile-main'
                    }
                    else if (params.ENVIRONMENT == 'dev') {
                        fileToLoad = 'pipelines/Jenkinsfile-dev'
                    }
                    else if (params.ENVIRONMENT == 'qa') {
                        fileToLoad = 'pipelines/Jenkinsfile-qa'
                    }
                    else if (params.ENVIRONMENT == 'stage') {
                        fileToLoad = 'pipelines/Jenkinsfile-stage'
                    }
                    else if (params.ENVIRONMENT == 'prod') {
                        fileToLoad = 'pipelines/Jenkinsfile-prod'
                    }

                    echo "Loading pipeline: ${fileToLoad}"

                    // Load the selected Jenkinsfile
                    load fileToLoad
                }
            }
        }
    }
}