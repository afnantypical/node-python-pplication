pipeline {
    agent any

    parameters {
        choice(name: 'APP_TYPE', choices: ['node', 'python'], description: 'Choose which app to deploy')
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to pull')
    }

    environment {
        EC2_USER = "ubuntu"
        EC2_IP = "44.213.75.159"
        SSH_KEY = "remote"   // Your credential ID from the screenshot
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: params.BRANCH_NAME,
                    url: 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        /* ------------------------ NODE DEPLOYMENT ------------------------ */

        stage('Deploy Node App') {
