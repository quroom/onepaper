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
        stage('Deploy to Staging') { 
            steps {
                sh 'cd /home/ubuntu/onepaper-green/; \
                git pull origin master; \
                pip install -r requirements --no-warn-script-location; \
                python manage.py migrate; \
                sudo service nginx reload; \
                sudo service onepaper-green restart "'
            }
        }
    }
}