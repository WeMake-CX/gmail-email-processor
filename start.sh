#!/bin/bash

# Define variables
MINICONDA_DIR="$HOME/miniconda3"
ENV_NAME="email_env"
REQUIRED_PACKAGES="tqdm mailbox"

# Function to download and install Miniconda
install_miniconda() {
    echo "Downloading and installing Miniconda..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if [[ $(uname -m) == 'arm64' ]]; then
            wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -O ~/miniconda.sh
        else
            wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
        fi
    else
        echo "Unsupported OS type: $OSTYPE"
        exit 1
    fi

    bash ~/miniconda.sh -b -u -p $MINICONDA_DIR
    rm ~/miniconda.sh
    $MINICONDA_DIR/bin/conda init bash
    source ~/.bashrc
}

# Check if Miniconda is already installed
if [ ! -d "$MINICONDA_DIR" ]; then
    install_miniconda
else
    echo "Miniconda is already installed."
fi

# Create and activate the virtual environment
echo "Creating and activating the virtual environment..."
$MINICONDA_DIR/bin/conda create --name $ENV_NAME python=3.8 -y
source $MINICONDA_DIR/bin/activate $ENV_NAME

# Install required packages
echo "Installing required packages..."
$MINICONDA_DIR/envs/$ENV_NAME/bin/pip install $REQUIRED_PACKAGES

echo "Setup complete. To activate the environment, run 'conda activate $ENV_NAME'."
