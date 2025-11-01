pipeline {

    agent any

    stages {

        stage("POR FAVOR FUNCIONA"){
            steps{
                echo 'PFV'
            }
        }
    
        stage('Build'){

            steps {
                echo 'Building...'
                sh "python3 --version"
                sh "pip3 --version"
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install -r requirements.txt
                   ls
                   '''

            }
        }
       
    }
    
}