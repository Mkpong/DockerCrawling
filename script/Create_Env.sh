ENV_NAME="dockerCrawling"
PYTHON_VERSION="3.9.19"

# 기존 Conda Env 제거
echo "Remove existing Conda virtual environment..."
conda env remove --name $ENV_NAME

# 새로운 Conda Env 생성
echo "Creating a Conda virtual environment..."
conda create -y -n $ENV_NAME python=$PYTHON_VERSION

echo "Activating the virtual environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

if [ -f "../requirement.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r ../requirement.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

# 설치 완료 메시지
echo "Environment setup complete! To activate the environment, use 'conda activate $ENV_NAME'."