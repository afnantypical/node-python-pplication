pipeline {
  agent any

  parameters {
    choice(name: 'APP_TYPE', choices: ['node', 'python'], description: 'Which app to deploy')
    string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch where the code lives (node, python, or main)')
  }

  environment {
    EC2_USER = "ubuntu"
    EC2_IP   = "44.213.75.159"
    SSH_KEY  = "remote"
  }

  stages {

    stage('Checkout Code') {
      steps {
        script {
          // Clean workspace
          deleteDir()

          // Checkout the branch specified by BRANCH_NAME
          checkout([
            $class: 'GitSCM',
            branches: [[ name: "refs/heads/${params.BRANCH_NAME}" ]],
            doGenerateSubmoduleConfigurations: false,
            extensions: [ [$class: 'CleanBeforeCheckout'] ],
            userRemoteConfigs: [[ url: 'https://github.com/afnantypical/node-python-pplication.git' ]]
          ])

          echo "Checked out branch: ${params.BRANCH_NAME}"
          sh "ls -R ."
        }
      }
    }

    stage('Deploy Node App') {
      when { expression { params.APP_TYPE == 'node' } }
      steps {
        sshagent([SSH_KEY]) {
          sh """
            # Ensure nodeapp folder exists
            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} 'sudo mkdir -p /var/www/nodeapp && sudo chmod -R 777 /var/www/nodeapp'

            scp -o StrictHostKeyChecking=no index.js ${EC2_USER}@${EC2_IP}:/var/www/nodeapp/

            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} '
              cd /var/www/nodeapp/
              sudo apt update -y
              sudo apt install -y nodejs npm
              npm install express axios || true
              nohup node index.js > node.log 2>&1 &
            '
          """
        }
      }
    }

    stage('Deploy Python App') {
      when { expression { params.APP_TYPE == 'python' } }
      steps {
        sshagent([SSH_KEY]) {
          sh """
            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} 'sudo mkdir -p /var/www/pyapp && sudo chmod -R 777 /var/www/pyapp'

            scp -o StrictHostKeyChecking=no app.py ${EC2_USER}@${EC2_IP}:/var/www/pyapp/

            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} '
              cd /var/www/pyapp/
              sudo apt install -y python3-venv
              if [ ! -d "venv" ]; then
                python3 -m venv venv
              fi
              ./venv/bin/pip install flask requests pandas
              nohup ./venv/bin/python app.py > flask.log 2>&1 &
            '
          """
        }
      }
    }

  }

  post {
    success {
      echo "Deployment finished successfully."
    }
    failure {
      echo "Deployment failed."
    }
  }
}
