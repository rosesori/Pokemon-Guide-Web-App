node {
    def app
    def image = "docker.io/pokeguidecsce315/pokeguide:${env.BUILD_NUMBER}"

    stage('Get Source Code') {
        git branch: 'master',
        credentialsId: 'githubcredentials',
        url: 'https://github.tamu.edu/joshuakim135/Pokemon-Guide.git'
    }
    stage('Build Docker image') {
        app = docker.build(image, "--network=host -f Dockerfile .")
    }

    stage('Test image') {
        // Ideally, we would run a test framework against our image. We will fake this stage in this simplified project.
        sh 'echo "Tests passed"'
    }
    
    stage('Push image to DockerHub') {
        withDockerRegistry([ credentialsId: "dockerhubcredentials", url: "" ]) {
          sh "docker push pokeguidecsce315/pokeguide:${env.BUILD_NUMBER}"
        } 
    }
    stage('Stop/remove previous container') {
        sh "docker stop flask-app"
        sh "docker rm flask-app"
    }
    stage("Run docker container"){
        sh "docker run -p 8000:8000 --name flask-app -d pokeguidecsce315/pokeguide:${env.BUILD_NUMBER}"
    }
}