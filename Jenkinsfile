updateGitlabCommitStatus state: 'pending'
pipeline {
    agent any
    options {
      gitLabConnection('gitlab-jenkins')
      gitlabBuilds(builds: ['build', 'test', 'deploy'])
    }
    post {
        failure {
            updateGitlabCommitStatus name: 'jenkins', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'jenkins', state: 'success'
        }
    }
    stages {
        stage('Build') { 
            steps {
                echo 'Jenkins Build'
                sh 'export PATH="/home/ubuntu/.nvm/versions/node/v15.5.0/bin:${PATH}"'
                sh 'pip3 install -r requirements.txt;'
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
            steps {
                echo 'Jenkins Staging'
                sh 'sudo su - ubuntu -c "cd /home/ubuntu/onepaper-green/; \
                git checkout master; \
                git pull --all; \
                git checkout -f $gitlabMergeRequestLastCommit; \
                git push --all old-origin \
                source /home/ubuntu/djangovenv/bin/activate; \
                pip3 install -r requirements.txt --no-warn-script-location; \
                unset Green; \
                cd frontend&&npm run build&&cd ..; \
                export DJANGO_DEBUG=False; \
                export USE_S3=True; \
                export DJANGO_PRODUCT=False; \
                python3 manage.py collectstatic --no-input -i admin -i summernote -i debug_toolbar -i rest_framework -i MaterialIcons* -i img/* -i css/* -i js/*; \
                unset DJANGO_DEBUG; \
                unset USE_S3;\
                python3 manage.py migrate; \
                sudo service nginx reload; \
                sudo service onepaper-green restart; \
                sudo rm -rf ~/web-info/cache/nginx/*; \
                sudo rm -rf ~/web-info/cache/nginx-green/*; \
                " '
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
    }
}