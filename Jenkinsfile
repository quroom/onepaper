pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                sh 'source /home/ubuntu/djangovenv/bin/activate; \
                pip3 install -r requirements.txt'
            }
        }
        stage('Test') { 
            steps {
                sh 'python3 manage.py test'
            }
        }
        stage('Deploy') { 
            steps {
                sh 'echo deploying'
            }
        }
    }
}