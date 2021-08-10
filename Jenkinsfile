pipeline {
  agent {
    kubernetes {
      yamlFile 'kubes-pod.yaml'
      defaultContainer 'ubuntu'
      activeDeadlineSeconds 3600
      idleMinutes 15
    }
  }
  stages {
    
    stage('Build') {
      steps {
        withCredentials([string(credentialsId: 'capstone-test-db-uri', variable: 'SQLALCHEMY_TEST_DATABASE_URI')]) {
          sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
          pytest --junitxml=junit.xml
          docker build -t docker.arpnetworking.com/capstone-backend .
          docker push docker.arpnetworking.com/capstone-backend
          '''
        }
      }
    }
  }
  post('Analysis') {
    always {
      junit 'junit.xml'
      recordIssues(
          enabledForFailure: true, aggregatingResults: true,
          tools: [pyLint(), junitParser(pattern: 'junit.xml')])
    }
  }
}
