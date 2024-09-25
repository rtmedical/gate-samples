# Use a imagem base opengatecollaboration/gate:9.4-docker
FROM opengatecollaboration/gate:9.4-docker

# Atualize os repositórios e instale Python3, pip, VNC, XFCE e dependências gráficas
RUN yum update -y && \
    yum install -y \
        python3 \
        python3-pip \
        tigervnc-server \
        xfce4 \
        xfce4-terminal \
        xorg-x11-apps \
        xorg-x11-fonts-Type1 \
        xorg-x11-utils \
        dbus-x11 \
    && yum clean all

# Definir variáveis de ambiente diretamente
ENV GATE_DIR=/software/gate
ENV ROOTSYS=/software/root-cern/install
ENV G4INSTALL=/software/geant4/install
ENV PATH=/software/gate/bin:/software/root-cern/install/bin:/software/geant4/install/bin:/software/cmake-3.18.4-Linux-x86_64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/software/gate/lib:/software/root-cern/install/lib:/software/geant4/install/lib:/software/cmake-3.18.4-Linux-x86_64/lib:$LD_LIBRARY_PATH

# Criar usuário para VNC
RUN useradd -m vncuser

# Definir variáveis de ambiente para VNC
ENV VNC_USER=vncuser
ENV VNC_PASS=vncpassword  # Senha padrão; pode ser sobrescrita via docker-compose.yml

# Copiar scripts para o contêiner
COPY entrypoint.sh /entrypoint.sh
COPY run_gate.sh /usr/local/bin/run_gate.sh

# Tornar os scripts executáveis
RUN chmod +x /entrypoint.sh /usr/local/bin/run_gate.sh

# Copiar arquivo de dependências Python
COPY requirements.txt /tmp/requirements.txt

# Instalar as bibliotecas Python
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Instalar o JupyterLab
RUN pip3 install jupyterlab

# Expor as portas para JupyterLab e VNC
EXPOSE 8888 5901

# Definir o entrypoint para usar o script personalizado
ENTRYPOINT ["/entrypoint.sh"]

# Definir o comando padrão como vazio, permitindo sobrescrever via docker-compose ou comandos
CMD []
