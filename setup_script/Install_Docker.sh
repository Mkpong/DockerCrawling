# 도커 설치 스크립트 for Ubuntu
DOCKER_VERSION="5:26.1.4-1~ubuntu.22.04~jammy"

echo "Removing old Docker versions..."
sudo apt-get remove -y docker docker-engine docker.io containerd runc

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

echo "Adding Docker’s official GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "Setting up the Docker stable repository..."
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Updating package index..."
sudo apt-get update

echo "Installing Docker 26.1.4..."
sudo apt-get install -y docker-ce=$DOCKER_VERSION docker-ce-cli=$DOCKER_VERSION containerd.io

echo "Verifying Docker version..."
docker --version

echo "Starting and enabling Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo "Adding current user to the Docker group..."
sudo usermod -aG docker $USER

echo "Docker installation is complete. Please log out and log back in to use Docker without sudo."

echo "Docker 26.1.4 installation and setup is complete!"