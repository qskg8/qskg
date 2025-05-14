#!/bin/bash

# 设置GitHub仓库的URL（请替换为你的实际仓库地址）
GITHUB_REPO_URL="https://github.com/your_username/your_repo.git"
SCRIPT_NAME="your_script.py"  # 你的Python脚本文件名

# 1. 安装screen（如果未安装）
if ! command -v screen &> /dev/null
then
    echo "screen未安装，正在安装..."
    sudo apt-get update
    sudo apt-get install -y screen
else
    echo "screen已安装"
fi

# 2. 安装pip（如果未安装）
if ! command -v pip &> /dev/null
then
    echo "pip未安装，正在安装..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
else
    echo "pip已安装"
fi

# 3. 创建ETH文件夹并进入该文件夹
mkdir -p ~/ETH
cd ~/ETH

# 4. 克隆GitHub上的脚本仓库
if [ ! -d "$SCRIPT_NAME" ]; then
    echo "从GitHub克隆仓库..."
    git clone $GITHUB_REPO_URL .
else
    echo "仓库已存在，跳过克隆步骤"
fi

# 5. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 6. 安装所需的Python库
pip install -r requirements.txt

# 7. 启动一个新的screen会话并在其中运行脚本
screen -dmS eth_scraper bash -c "python3 $SCRIPT_NAME"

# 提示信息
echo "已创建文件夹并启动screen会话。脚本正在运行中。"
