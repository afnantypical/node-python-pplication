pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'APP_TYPE', choices: ['Node', 'Python'], description: 'Select which app to deploy')
    }

    environment {
        NODE_APP_DIR = "/var/www/nodeapp"
        PYTHON_APP_DIR = "/var/www/pyapp"
        REMOTE_USER = "ubuntu"
        REMOTE_HOST = "44.213.75.159"
        SSH_CREDENTIALS = "ubuntu"  // Jenkins SSH credential ID
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Checkout selected branch
                git branch: "${params.BRANCH}", url: 'https://github.com/afnantypical/node-python-pplication.git'
                sh 'ls -R .'  // list files for debug
            }
        }

        stage('Deploy Node App') {
            when {
                expression { params.APP_TYPE == 'Node' }
            }
            steps {
                sshagent([env.SSH_CREDENTIALS]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'sudo mkdir -p ${NODE_APP_DIR} && sudo chmod -R 777 ${NODE_APP_DIR}'
                        scp -o StrictHostKeyChecking=no app.js ${REMOTE_USER}@${REMOTE_HOST}:${NODE_APP_DIR}/
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'nohup node ${NODE_APP_DIR}/app.js > ${NODE_APP_DIR}/node.log 2>&1 &'
                    """
                }
            }
        }

        stage('Deploy Python App') {
            when {
                expression { params.APP_TYPE == 'Python' }
            }
            steps {
                sshagent([env.SSH_CREDENTIALS]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'sudo mkdir -p ${PYTHON_APP_DIR} && sudo chmod -R 777 ${PYTHON_APP_DIR}'
                        scp -o StrictHostKeyChecking=no app.py ${REMOTE_USER}@${REMOTE_HOST}:${PYTHON_APP_DIR}/
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'nohup python3 ${PYTHON_APP_DIR}/app.py > ${PYTHON_APP_DIR}/python.log 2>&1 &'
                    """
                }
            }
        }

    }

    post {
        success {
            echo "Deployment of ${params.APP_TYPE} app from branch ${params.BRANCH} succeeded!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
