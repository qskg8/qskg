#!/bin/bash

# 1. 在根目录创建 ETH 文件夹
echo "创建 ETH 文件夹..."
mkdir -p /ETH

# 2. 进入 ETH 文件夹
cd /ETH

# 3. 下载 eth.pyc 文件
echo "下载 eth.pyc 文件..."
curl -L -o eth.pyc https://github.com/qskg8/qskg/blob/%E8%BD%BB%E6%9D%BE%E7%9F%BF%E5%B7%A5/eth.pyc?raw=true

# 4. 安装虚拟环境
echo "安装虚拟环境..."
apt update
apt install python3-venv -y

# 5. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 6. 安装 pip3
echo "安装 pip3..."
apt install python3-pip -y

# 7. 安装依赖项
echo "安装依赖项..."
pip3 install requests mysql-connector-python playwright

# 8. 安装 Playwright 浏览器二进制文件
echo "安装 Playwright 浏览器二进制文件..."
playwright install

# 9. 安装 Playwright 依赖项
echo "安装 Playwright 依赖项..."
playwright install-deps

# 10. 安装 screen
echo "安装 screen..."
apt install screen -y

# 11. 启动一个 screen 会话
echo "启动 screen 会话..."
screen -S eth_session -d -m bash -c "cd /ETH && python3 eth.pyc"

echo "脚本执行完成，screen 会话已启动，eth.pyc 正在运行..."
