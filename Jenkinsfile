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
        stage('Build and Test') {
            when { expression { env.gitlabSourceBranch != 'master' } }
            steps {
                echo 'Jenkins Build and Test'
                sh 'cp /var/jenkins_home/.env .env'
                sh 'docker build -t djangovue_test --network onepaper_default -f Dockerfile-test .'
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
        stage('Deploy to Staging') {
            when { expression { env.gitlabSourceBranch != 'master' } }
            steps {
                echo 'Jenkins Staging'
                sh 'docker run -i djangovue_test python manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons*;'
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@dev.onepaper.biz "cd /home/ubuntu/onepaper/; \
                git checkout .; \
                git checkout master; \
                git pull --all; \
                git checkout -f $gitlabMergeRequestLastCommit; \
                git push -f --all old-origin; \
                sudo docker-compose -f docker-compose.staging.yml exec -T django python3 manage.py migrate; \
                sudo docker-compose -f docker-compose.staging.yml restart django; \
                sudo docker-compose -f docker-compose.staging.yml exec -T nginx-proxy nginx -s reload; \
                sudo docker-compose -f docker-compose.staging.yml exec -T nginx-proxy sh -c \'rm -rf /etc/nginx/cache/*\'" '
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
                submitter "admin"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@onepaper.biz "source djangovenv/bin/activate; \
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
        stage('Switch Blue to Green and deploy Blue') {
            when { 
                beforeInput true
                expression { env.gitlabSourceBranch == 'master' } 
            }
            input {
                message "Shall we switch blue to green?"
                submitter "admin"
            }
            steps {
                //Switch Blue to green
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@onepaper.biz "source djangovenv/bin/activate; \
                cd onepaper; \
                git checkout .; \
                git pull origin master; \
                sh config/nginx/blue-green-deploy.sh g; \
                sudo systemctl reload nginx;" '

                //Deploy to Blue : Deploy static file.
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@dev.onepaper.biz "cd /home/ubuntu/onepaper/; \
                git checkout .; \
                git checkout master; \
                git pull origin master; \
                sudo docker build -t djangovue_test -f Dockerfile-test .; \
                sudo docker run -i -e GREEN=False djangovue_test python manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons*;" '
                //Deploy to Blue : Deploy django server.
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@onepaper.biz "source djangovenv/bin/activate; \
                cd onepaper; \
                git checkout .; \
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
                submitter "admin"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no ubuntu@54.180.203.148 "source djangovenv/bin/activate; \
                cd onepaper; \
                git checkout .; \
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