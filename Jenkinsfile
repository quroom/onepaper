updateGitlabCommitStatus state: 'pending'
pipeline {
    agent any
    options {
      gitLabConnection('gitlab-jenkins')
    }
    post {
        failure {
            updateGitlabCommitStatus name: 'jenkins', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'jenkins', state: 'success'
        }
        aborted {
            updateGitlabCommitStatus name: 'jenkins', state: 'canceled'
        }
    }
    stages {
        stage('Build') {
            when { expression { env.gitlabSourceBranch != 'master' } }
            steps {
                echo 'Jenkins Build'
                sh 'pip3 install -r requirements.txt;'
                sh 'cd frontend; npm install; npm run build;'
            }
            post {
                failure {
                    updateGitlabCommitStatus name: 'build', state: 'failed'
                }
                success {
                    updateGitlabCommitStatus name: 'build', state: 'success'
                }
            }
        }
        stage('Test') {
            when { expression { env.gitlabSourceBranch != 'master' } }
            steps {
                echo 'Jenkins Test'
                sh 'export DJANGO_HTTP=True; \
                python3 manage.py test;'
            }
            post {
                failure {
                    updateGitlabCommitStatus name: 'test', state: 'failed'
                }
                success {
                    updateGitlabCommitStatus name: 'test', state: 'success'
                }
            }
        }
        stage('Deploy to Staging') {
            when { expression { env.gitlabSourceBranch != 'master' } }
            steps {
                echo 'Jenkins Staging'
                sh 'sudo su - ubuntu -c "cd /home/ubuntu/onepaper-green/; \
                git checkout master; \
                git pull --all; \
                git checkout -f $gitlabMergeRequestLastCommit; \
                git push --all old-origin; \
                source /home/ubuntu/djangovenv/bin/activate; \
                pip3 install -r requirements.txt --no-warn-script-location; \
                unset Green; \
                cd frontend; npm install; npm run build; cd ..; \
                export DJANGO_DEBUG=False; export USE_S3=True; export DJANGO_PRODUCT=False; \
                python3 manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons* -i img/* -i css/* -i js/*; \
                unset DJANGO_DEBUG; unset USE_S3; \
                python3 manage.py migrate; \
                sudo service nginx reload; \
                sudo service onepaper-green restart; \
                sudo rm -rf ~/web-info/cache/nginx/*; \
                sudo rm -rf ~/web-info/cache/nginx-green/*;" '
            }
            post {
                failure {
                    updateGitlabCommitStatus name: 'deploy', state: 'failed'
                }
                success {
                    updateGitlabCommitStatus name: 'deploy', state: 'success'
                }
            }
        }
        // Deploy to Production
        stage('Deploy to Green') {
            when { 
                beforeInput true
                expression { env.gitlabSourceBranch == 'master' } 
            }
            input {
                message "Shall we deploy to green production?"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@54.180.203.148 "source djangovenv/bin/activate; \
                cd onepaper-green; \
                git pull origin master; \
                pip install -r requirements.txt --no-warn-script-location; \
                python manage.py migrate; \
                deactivate; \
                sudo systemctl restart onepaper-green; \
                sudo systemctl reload nginx; \
                sudo rm -rf ~/web-info/cache/nginx-green/*;" '
            }
            post {
                aborted {
                    updateGitlabCommitStatus name: 'jenkins', state: 'canceled'
                }
            }
        }
        stage('Switch Blue to Green') {
            when { 
                beforeInput true
                expression { env.gitlabSourceBranch == 'master' } 
            }
            input {
                message "Shall we switch blue to green?"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@54.180.203.148 "source djangovenv/bin/activate; \
                cd onepaper; \
                git pull origin master; \
                sh config/nginx/blue-green-deploy.sh g; \
                sudo systemctl reload nginx;" '
            }
            post {
                aborted {
                    updateGitlabCommitStatus name: 'jenkins', state: 'canceled'
                }
            }
        }
        stage('Deploy to Blue') {
            when { 
                beforeInput true
                expression { env.gitlabSourceBranch == 'master' } 
            }
            input {
                message "Shall we deploy to blue production?"
            }
            steps {
                sh 'sudo su - ubuntu -c "cd /home/ubuntu/onepaper/; \
                git checkout master; \
                git pull origin master; \
                source /home/ubuntu/djangovenv/bin/activate; \
                export Green=False; \
                cd frontend; npm install; npm run build; cd ..; \
                export DJANGO_DEBUG=False; export USE_S3=True; export DJANGO_PRODUCT=False; \
                python3 manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons* -i img/* -i css/* -i js/*; \
                unset DJANGO_DEBUG; \
                unset USE_S3;" '
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@54.180.203.148 "source djangovenv/bin/activate; \
                cd onepaper; \
                git pull origin master; \
                deactivate; \
                sudo systemctl restart onepaper; \
                sudo systemctl reload nginx; \
                sudo rm -rf ~/web-info/cache/nginx/*;" '
            }
            post {
                aborted {
                    updateGitlabCommitStatus name: 'jenkins', state: 'canceled'
                }
            }
        }
        stage('Switch Green to Blue') {
            when { 
                beforeInput true
                expression { env.gitlabSourceBranch == 'master' } 
            }
            input {
                message "Shall we switch blue to green?"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@54.180.203.148 "source djangovenv/bin/activate; \
                cd onepaper; \
                git pull origin master; \
                sh config/nginx/blue-green-deploy.sh b; \
                sudo systemctl reload nginx;" '
            }
            post {
                aborted {
                    updateGitlabCommitStatus name: 'jenkins', state: 'canceled'
                }
            }
        }
    }
}