FROM debian:stretch

# Install compilation and testing dependencies #################################
RUN apt-get update     -qq                                                      && \
    apt-get install -y -qq curl                                                 && \
    apt-get install -y -qq gnupg

# Add apt-get repositories containing required packages. ###########################
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN echo "deb http://deb.debian.org/debian testing main" \
  | tee /etc/apt/sources.list.d/python3_6.list
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt " \
  "stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list

# Install apt dependencies. ####################################################
RUN apt-get update -qq                                                      && \
    apt-get upgrade -y -qq                                                  && \
    apt-get install -y                                                         \
    ant                                                                        \
    autoconf                                                                   \
    autoconf                                                                   \
    automake                                                                   \
    bazel                                                                      \
    bmon                                                                       \
    build-essential                                                            \
    ca-certificates-java                                                       \
    check                                                                      \
    clang-3.9                                                                  \
    clang-format-7                                                             \
    cmake                                                                      \
    g++                                                                        \
    git                                                                        \
    google-perftools                                                           \
    gphoto2                                                                    \
    gphotofs                                                                   \
    htop                                                                       \
    libc++-dev                                                                 \
    libc++abi-dev                                                              \
    lib32z1-dev                                                                \
    libc6-dev-i386                                                             \
    libgoogle-perftools-dev                                                    \
    librsync-dev                                                               \
    libssl-dev                                                                 \
    lsb-release                                                                \
    libtool                                                                    \
    libyajl-dev                                                                \
    libz-dev                                                                   \
    make                                                                       \
    nodejs                                                                     \
    pkg-config                                                                 \
    protobuf-compiler                                                          \
    python2.7                                                                  \
    python2.7-lib                                                              \
    python2.7-dev                                                              \
    python3.7                                                                  \
    python3.7-dev                                                              \
    python3.7-distutils                                                        \
    python-matplotlib                                                          \
    python-empy                                                                \
    python-jinja2                                                              \
    ruby                                                                       \
    screen                                                                     \
    sudo                                                                       \
    tmux                                                                       \
    uthash-dev                                                                 \
    vim

# Install pip and python dependencies. #########################################
RUN curl https://bootstrap.pypa.io/get-pip.py | python2.7
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN pip2.7 install --upgrade pip                                            && \
    pip3.6 install --upgrade pip

# Set up workspace. ############################################################
# Fix xlocale.h renamed to locale.h
# https://bugs.launchpad.net/ubuntu/+source/libc++/+bug/1725858
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN useradd -ms /bin/bash illuminate
RUN echo 'illuminate:illuminate' | chpasswd
RUN echo "%sudo  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN usermod -aG sudo illuminate

# User env setup. ##############################################################
RUN mkdir /external_libs

RUN apt-get install -y openssh-client openssh-server

USER illuminate
RUN mkdir -p /home/illuminate/code_env
ENV WORKSPACE /home/illuminate/code_env WORKDIR /home/illuminate/code_env

WORKDIR /home/illuminate

# Install python requirements. #################################################
RUN pip2.7 install --user future

RUN pip2.7 install --user                                                      \
  future==0.16.0                                                               \
  Flask==0.12.2                                                                \
  Flask-SocketIO==2.9.2                                                        \
  futures==3.1.1                                                               \
  socketIO-client==0.7.2                                                       \
  numpy==1.15.2                                                                \
  empy==3.3.2                                                                  \
  toml==0.9.4                                                                  \
  eventlet==0.23.0                                                             \
  protobuf==3.5.2.post1                                                        \
  pyzmq==17.0.0                                                                \
  zmq==0.0.0

# Set up working directory and permissions for later scripts to use. ###########
WORKDIR /home/illuminate/code_env

# Set user to root so that we can set the appropriate permissions for file #####
# access later on. #############################################################
USER root
