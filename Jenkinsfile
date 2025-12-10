pipeline {
    agent any

    parameters {
        choice(name: 'APP', choices: ['node.js', 'app.py'], description: 'Select which app to deploy')
    }

    environment {
        PYTHON_VENV = "${WORKSPACE}/venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/afnantypical/node-python-pplication.git'
                sh 'ls -R .'
            }
        }

        stage('Setup Environment') {
            when { expression { params.APP == 'app.py' } }
            steps {
                echo 'Setting up Python environment...'
                sh '''
                # Install venv if missing (Debian/Ubuntu)
                sudo apt-get update
                sudo apt-get install -y python3-venv python3-pip python3-distutils

                # Create venv
                python3 -m venv venv
                source venv/bin/activate

                # Upgrade pip and install packages
                pip install --upgrade pip
                pip install flask requests pandas
                '''
            }
        }

        stage('Deploy Node App') {
            when { expression { params.APP == 'node.js' } }
            steps {
                sh '''
                echo "Starting Node.js app..."

                # Kill previous node process if exists
                pkill -f app.js || true

                # Install Node dependencies
                if [ -f package.json ]; then
                    npm install
                fi

                # Run Node app in background
                nohup node app.js > node_app.log 2>&1 &
                '''
            }
        }

        stage('Deploy Python App') {
            when { expression { params.APP == 'app.py' } }
            steps {
                sh '''
                echo "Starting Python Flask app..."

                # Kill previous Python process if exists
                pkill -f app.py || true

                # Activate venv and run app
                source venv/bin/activate
                nohup python3 app.py > python_app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment of ${params.APP} succeeded!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
