pipeline {
    agent any

    parameters {
        choice(
            name: 'APP_TYPE',
            choices: ['app.py', 'node.js'],
            description: 'Select which app to deploy'
        )
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "main", url: 'https://github.com/afnantypical/node-python-pplication.git'
                sh 'ls -R .'    // Debug to verify files
            }
        }

        stage('Deploy Node App') {
            when {
                expression { params.APP_TYPE == 'node.js' }
            }
            steps {
                sh '''
                    echo "Starting Node Application..."

                    # Kill old running Node app
                    pkill -f app.js || true

                    # Install dependencies if package.json exists
                    if [ -f package.json ]; then
                        npm install
                    fi

                    # Start Node app
                    nohup node app.js > node_app.log 2>&1 &
                '''
            }
        }

        stage('Deploy Python App') {
            when {
                expression { params.APP_TYPE == 'app.py' }
            }
            steps {
                sh '''
                    echo "Starting Python Application..."

                    # Kill old Python app
                    pkill -f app.py || true

                    # Install requirements
                    if [ -f requirements.txt ]; then
                        pip3 install -r requirements.txt
                    fi

                    # Start Python app
                    nohup python3 app.py > python_app.log 2>&1 &
                '''
            }
        }

    }

    post {
        success {
            echo "Deployment of ${params.APP_TYPE} succeeded!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
