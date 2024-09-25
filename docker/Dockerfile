# Use a imagem base opengatecollaboration/gate
FROM opengatecollaboration/gate:9.4-docker

# Atualize os repositórios e instale o Python3 e pip
RUN yum update -y && \
    yum install -y python3 python3-pip && \
    yum clean all

# Instalando Tela para elimiar erros de execução do GATE 
# Atualize os repositórios e instale o Python3, pip, PyQt5 e Xvfb
RUN yum update -y && \
    yum install -y \
        xorg-x11-server-Xvfb \
        libXrender \
        libXext \
        libSM \
        libICE \
        libX11 \
        libXrandr \
        libXcursor \
        libXi \
    && yum clean all

# Instale as bibliotecas Python a partir do requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Instale o Jupyter Notebook
RUN pip3 install jupyterlab

# Copie o script de entrada personalizado para o contêiner
COPY entrypoint.sh /entrypoint.sh

# Torne o script de entrada executável
RUN chmod +x /entrypoint.sh

# Mantenha o script original runGate.sh (já presente na imagem base)

# Defina o entrypoint para usar o script personalizado
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8888

# Defina o comando padrão como vazio, permitindo sobrescrever via docker-compose ou comandos
CMD []
