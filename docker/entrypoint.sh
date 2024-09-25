#!/bin/bash
# entrypoint.sh

# Saia imediatamente se algum comando falhar
set -e

# Configurar VNC
# Definir DISPLAY
export DISPLAY=:1

# Configurar senha do VNC
mkdir -p /home/$VNC_USER/.vnc
echo "$VNC_PASS" | vncpasswd -f > /home/$VNC_USER/.vnc/passwd
chmod 600 /home/$VNC_USER/.vnc/passwd
chown -R $VNC_USER:$VNC_USER /home/$VNC_USER/.vnc

# Criar arquivo xstartup para iniciar XFCE
echo "#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &" > /home/$VNC_USER/.vnc/xstartup
chmod +x /home/$VNC_USER/.vnc/xstartup
chown $VNC_USER:$VNC_USER /home/$VNC_USER/.vnc/xstartup

# Iniciar o servidor VNC como vncuser
su - $VNC_USER -c "vncserver :1 -geometry 1280x800 -depth 24"

# Iniciar o JupyterLab
jupyter lab --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' &

# Manter o contêiner ativo
tail -f /dev/null
