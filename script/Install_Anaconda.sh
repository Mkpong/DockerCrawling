ANACONDA_VERSION="2023.03"
ANACONDA_INSTALLER="Anaconda3-$ANACONDA_VERSION-Linux-x86_64.sh"
DOWNLOAD_URL="https://repo.anaconda.com/archive/$ANACONDA_INSTALLER"

INSTALL_PATH="$HOME/anaconda3"

echo "Downloading Anaconda installer..."
wget $DOWNLOAD_URL -O $ANACONDA_INSTALLER

chmod +x $ANACONDA_INSTALLER

# 아나콘다 설치 (yes 옵션을 통해 자동으로 수락)
echo "Installing Anaconda..."
./$ANACONDA_INSTALLER -b -p $INSTALL_PATH

echo "Configuring Anaconda..."
export PATH="$INSTALL_PATH/bin:$PATH"

echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc

# 아다 설치파일 삭제
rm -rf $ANACONDA_INSTALLER

source ~/.bashrc

echo "Anaconda installation complete!"

conda --version