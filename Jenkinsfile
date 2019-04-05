pipeline {
  agent { label 'ubuntu-18.04' }
  triggers { upstream( upstreamProjects: 'IncludeOS/IncludeOS/master, IncludeOS/IncludeOS/dev', threshold: hudson.model.Result.SUCCESS ) }
  options { checkoutToSubdirectory('src') }
  environment {
    CONAN_USER_HOME = "${env.WORKSPACE}"
    PROFILE_x86_64 = 'clang-6.0-linux-x86_64'
    PROFILE_x86 = 'clang-6.0-linux-x86'
    CPUS = """${sh(returnStdout: true, script: 'nproc')}"""
    PACKAGE = 'vmbuild'
    USER = 'includeos'
    CHAN_LATEST = 'latest'
    CHAN_STABLE = 'stable'
    REMOTE = "${env.CONAN_REMOTE}"
    BINTRAY_CREDS = credentials('devops-includeos-user-pass-bintray')
    SRC = "${env.WORKSPACE}/src"
  }

  stages {
    stage('Setup') {
      steps {
        sh script: "ls -A | grep -v src | xargs rm -r || :", label: "Clean workspace"
        sh script: "conan config install https://github.com/includeos/conan_config.git", label: "conan config install"
      }
    }
    stage('Build package') {
      steps {
        build_conan_package("$PROFILE_x86_64")
        script { VERSION = sh(script: "conan inspect -a version $SRC | cut -d ' ' -f 2", returnStdout: true).trim() }
      }
    }
    stage('Upload to bintray') {
      parallel {
        stage('Latest release') {
          when { branch 'master' }
          steps {
            upload_package("$CHAN_LATEST")
          }
        }
        stage('Stable release') {
          when { buildingTag() }
          steps {
            sh script: "conan copy --all $PACKAGE/$VERSION@$USER/$CHAN_LATEST $USER/$CHAN_STABLE", label: "Copy to stable channel"
            upload_package("$CHAN_STABLE")
          }
        }
      }
    }
  }
}


def build_conan_package(String profile) {
  sh script: "conan create $SRC $USER/$CHAN_LATEST -pr ${profile}", label: "Build with profile: $profile"
}

def upload_package(String channel) {
  sh script: """
    conan user -p $BINTRAY_CREDS_PSW -r $REMOTE $BINTRAY_CREDS_USR
    conan upload --all -r $REMOTE $PACKAGE/$VERSION@$USER/$channel
  """, label: "Upload to bintray"
}
