pipeline {

    agent any

    stages {

        stage('Build'){

            steps {
                echo 'Building...'
                sh "python --version"
                sh "pip --version"
                sh '''
                   python -m venv venv
                   . venv/bin/activate
                   pip install -r requirements.txt
                   ls
                   '''

            }
        }
        
    }
}