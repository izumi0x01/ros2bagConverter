
# 必要となるubuntuのバージョンに応じてベースのイメージを変更してください
FROM ubuntu:22.04

# 環境設定
ENV DEBIAN_FRONTEND=noninteractive

# タイムゾーンの設定
#RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Tokyo 

# パッケージの更新
RUN apt-get update && apt-get upgrade -y && \
    apt-get install sudo -y

# GUIを使うためのライブラリ
RUN apt-get install x11-apps -y

# ros2インストール
RUN apt-get install curl gnupg lsb-release -y && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [ arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg ] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" > /etc/apt/sources.list.d/ros2.list && \
    apt-get update && \
    apt-get install -y \
    ros-humble-desktop \
    python3-colcon-common-extensions \
    ros-humble-rosbridge-suite && \
    apt-get install -y tmux vim python3.9 python3-pip curl

# ユーザー追加+ワークスペース作成
# load arguments from .env and docker-compose.yml
ARG UID GID USERNAME GROUPNAME PASSWORD
ARG WS=/home/$USERNAME/dev_ws
RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID -G sudo $USERNAME && \
    echo $USERNAME:$PASSWORD | chpasswd && \
    echo "$USERNAME  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER $USERNAME
WORKDIR $WS
RUN . /opt/ros/humble/setup.sh && colcon build && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc


# stop alert bell
RUN touch ~/.inputrc && \
    echo "# quit beep sound" >> ~/.inputrc && \
    echo "set bell-style none" >> ~/.inputrc

RUN pip3 install --no-cache-dir \
    black \
    jupyterlab \
    #nodejs \
    jupyterlab-lsp \
    'python-lsp-server[all]' \
    lckr-jupyterlab-variableinspector \
    jupyterlab_code_formatter \
    jupyterlab-git \
    jupyterlab_widgets \
    ipywidgets \
    import-ipynb
#notebook

# COPY requirements.txt /home/$USERNAME
#COPY requirements.txt $WS

# install pip
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools

# install python libraries
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
