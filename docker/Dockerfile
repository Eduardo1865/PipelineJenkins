# Define nossa imagem base
FROM jenkins/jenkins:lts

# Define nosso usuario dentro do container
USER root

# Atualiza os pacotes do sistema
RUN apt-get update

# Instala Python e pip
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv


# Da permissão para o usuário jenkins
RUN chown -R jenkins:jenkins /usr/local

# Limpa arquivos baixados com apt-get
RUN apt-get clean

USER jenkins