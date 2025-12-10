pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'node-python-pplication', choices: ['app.py', 'node.js'], description: 'Select which app to deploy')
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${params.BRANCH}", url: 'https://github.com/afnantypical/node-python-pplication.git'
                sh 'ls -R .'   // Debug to confirm files
            }
        }

        stage('Deploy Node App') {
            when {
                expression { params.node-python-pplication == 'node.js' }
            }
            steps {
                sh """
                    echo 'Starting Node Application...'

                    # Kill old Node process (if running)
                    pkill -f app.js || true

                    # Install dependencies if package.json exists
                    if [ -f package.json ]; then
                        npm install
                    fi

                    # Run Node App
                    nohup node app.js > node_app.log 2>&1 &
                """
            }
        }

        stage('Deploy Python App') {
            when {
                expression { params.node-python-pplication == 'app.py' }
            }
            steps {
                sh """
                    echo 'Starting Python Application...'

                    # Kill old Python process (if running)
                    pkill -f app.py || true

                    # Install Python requirements if file exists
                    if [ -f requirements.txt ]; then
                        pip3 install -r requirements.txt
                    fi

                    # Run Python App
                    nohup python3 app.py > python_app.log 2>&1 &
                """
            }
        }
    }

    post {
        success {
            echo "Deployment of ${params.node-python-pplication} app from branch ${params.BRANCH} succeeded!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
