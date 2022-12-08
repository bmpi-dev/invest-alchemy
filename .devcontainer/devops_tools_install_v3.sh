#!/bin/bash

# source <(curl -s https://raw.githubusercontent.com/chilcano/how-tos/master/src/devops_tools_install_v3.sh) -a=arm -t=0.11.15-oci -p=1.5.5

echo "##########################################################"
echo "####         Install and setup DevOps tools v3        ####"
echo "##########################################################"

while [ $# -gt 0 ]; do
  case "$1" in
    --arch*|-a*)                           # amd | arm 
      if [[ "$1" != *=* ]]; then shift; fi 
      _ARCH="${1#*=}"
      ;;
    --tf-ver*|-t*)
      if [[ "$1" != *=* ]]; then shift; fi
      _TF_VER="${1#*=}"
      ;;
    --packer-ver*|-p*)
      if [[ "$1" != *=* ]]; then shift; fi
      _PACKER_VER="${1#*=}"
      ;; 
    --help|-h)
      printf "\t Install DevOps tools. \n"
      printf "\t Examples: \n"
      printf "\t . devops_tools_install_v3.sh --arch=amd --tf-ver=0.11.15-oci \n"
      printf "\t . devops_tools_install_v3.sh --arch=amd --tf-ver=0.12.26 \n"
      printf "\t . devops_tools_install_v3.sh --arch=arm --packer-ver=1.5.5 \n"
      exit 0
      ;;
    *)
      >&2 printf "\t Error: Invalid argument. \n"
      exit 1
      ;;
  esac
  shift
done

export DEBIAN_FRONTEND=noninteractive

ARCH="${_ARCH:-amd}"

echo "==> Installing Git, curl, jq, unzip, software-properties-common and tree"
sudo apt -yqq update
sudo apt -yqq upgrade
sudo apt -yqq install git curl jq unzip software-properties-common sudo apt-transport-https tree > "/dev/null" 2>&1
printf ">> Git, curl, jq and unzip installed.\n\n"

echo "==> Installing AWS CLI v2.x"
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip ./aws
printf ">> '$(aws --version)' installed.\n\n"

# Disabled installation of Ansible (Ubuntu 20.04 has issues)
#echo "==> Installing Ansible"
#sudo apt-add-repository --yes --update ppa:ansible/ansible
#sudo apt -yqq install ansible
#printf ">> Ansible installed.\n\n"

echo "==> Installing Java 8 and 11 (default)"
sudo apt -yqq install default-jdk openjdk-8-jdk > "/dev/null" 2>&1
##sudo add-apt-repository --yes --update ppa:linuxuprising/java
##sudo apt -yqq install oracle-java11-installer-local
printf ">> Java installed.\n\n"

echo "==> Selecting the default Java/Javac version and auto-mode"
if [[ "$ARCH" = "arm" ]]; then
  sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-armhf/jre/bin/java 1200
  sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-8-openjdk-armhf/bin/javac 1200
else 
  ## Selecting manually the java version
  # sudo update-alternatives --config java
  # sudo update-alternatives --config javac

  ## Java-8
  #sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java 1200
  #sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-8-openjdk-amd64/bin/javac 1200
  
  ## Java-11
  sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-11-openjdk-amd64/bin/java 1111
  sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-11-openjdk-amd64/bin/javac 1111
fi
printf "\n\n"

echo "==> Installing Maven"
sudo apt -yqq install maven > "/dev/null" 2>&1
printf ">> Maven installed.\n\n"

echo "==> Creating '/etc/profile.d/maven.sh'"
cat << 'EOF' > maven.sh
#!/bin/bash

JAVA_HOME=/usr/lib/jvm/default-java
M2_HOME=/opt/maven
MAVEN_HOME=/opt/maven
## removed 'export' and replaced '${xyz}' for '$xyz'
PATH=$M2_HOME/bin:$PATH
EOF
sudo chown -R root:root maven.sh
sudo chmod +x maven.sh
sudo mv maven.sh /etc/profile.d/maven.sh
. /etc/profile.d/maven.sh
printf ">> Java and Maven configured.\n"
mvn -version
printf "\n\n"

echo "==> Installing Golang"
sudo apt -yqq install golang > "/dev/null" 2>&1
printf ">> Golang ($(go version)) installed.\n\n"

echo "==> Installing Terraform"
#_TF_VER="0.11.15-oci"
TF_VER_LATEST=$(curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r -M '.current_version')
TF_VER="${_TF_VER:-$TF_VER_LATEST}"
if [[ "$ARCH" =  "arm" ]]; then
  TF_BUNDLE="terraform_${TF_VER}_linux_${ARCH}.zip"
else
  TF_BUNDLE="terraform_${TF_VER}_linux_${ARCH}64.zip"
fi
wget --quiet "https://releases.hashicorp.com/terraform/${TF_VER}/${TF_BUNDLE}"
unzip -q "${TF_BUNDLE}"
sudo mv terraform /usr/local/bin/
rm -rf terraf*
printf ">> $(terraform version) installed.\n\n"

echo "==> Installing Packer"
#PACKER_VER="1.5.5"
PACKER_VER_LATEST=$(curl -s https://checkpoint-api.hashicorp.com/v1/check/packer | jq -r -M '.current_version')
PACKER_VER="${_PACKER_VER:-$PACKER_VER_LATEST}"
if [[ "$ARCH" = "arm" ]]; then
  PACKER_BUNDLE="packer_${PACKER_VER}_linux_${ARCH}.zip"
else
  PACKER_BUNDLE="packer_${PACKER_VER}_linux_${ARCH}64.zip"
fi
wget --quiet "https://releases.hashicorp.com/packer/${PACKER_VER}/${PACKER_BUNDLE}"
unzip -q "${PACKER_BUNDLE}"
sudo mv packer /usr/local/bin/
rm -rf packer*
printf ">> $(packer version) installed.\n\n"

echo "==> Installing Docker"
sudo apt -yqq install docker.io > "/dev/null" 2>&1
sudo systemctl enable --now docker
sudo apt-mark hold docker.io
sudo usermod -aG docker $USER
DOCKER_VER="$(curl -s --unix-socket /var/run/docker.sock http://latest/version | jq -r -M '.Version')"
printf ">> Docker ${DOCKER_VER} installed.\n\n"

echo "==> Installing NodeJS, NPM and AWS CDK"
sudo apt -yqq install nodejs npm > "/dev/null" 2>&1
sudo npm install --quiet -g aws-cdk > "/dev/null" 2>&1
printf ">> NodeJS $(npm -v node), NPM $(npm -v npm) and AWS CDK $(cdk --version) installed.\n\n"

echo "==> Installing Python3, Python3-Pip and Dev tools"
sudo apt -yqq install python3 python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv > "/dev/null" 2>&1
printf ">> $(python3 --version) installed.\n\n"

printf ">> End!! \n\n"