
FROM ubuntu:22.04

ARG UID_NUMBER=1001
ARG SPTUSER
ARG SPTHOME=/home/${SPTUSER}
#ARG MINICONDA_PATH=${SPTHOME}/miniconda
ARG MINICONDA_PATH=/opt/miniconda
ARG MINICONDA_INSTALL_FILE=Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
ENV MINICONDA_PATH ${MINICONDA_PATH}


RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends
RUN apt-get update --fix-missing
RUN apt-get update && apt-get install -yq --no-install-recommends \
    apt-utils \
    build-essential \
    default-jre \
    default-libmysqlclient-dev \
    dnsutils \
    gfortran \
    gsl-bin \
    libeigen3-dev \
    libgsl0-dev \
    nfs-common \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -yq --no-install-recommends \
    wget \
    ucommon-utils \
    coreutils

RUN useradd -ms /bin/bash -u 1001 $SPTUSER && \
    addgroup wheel && \
    addgroup -gid 1003 spt

# Add $SPTUSER to wheel and spt
RUN usermod -aG wheel $SPTUSER && \
    usermod -aG spt $SPTUSER

# Make mount directory to mirror /data/spt3g
RUN mkdir -p /data/skyviewer && \
    chgrp spt /data/skyviewer && \
    chmod g+wrx /data/skyviewer

# Use entrypoint script to start with conda and spt_cutter initialized
COPY ubuntu/startup.sh /opt/startup.sh
RUN chmod a+x /opt/startup.sh

# Conda installation, using python38
RUN mkdir -p ${MINICONDA_PATH} \
    && cd ${MINICONDA_PATH} \
    && wget https://repo.anaconda.com/miniconda/${MINICONDA_INSTALL_FILE} \
    && chmod +x ${MINICONDA_INSTALL_FILE} \
    && ./${MINICONDA_INSTALL_FILE} -b -p ${MINICONDA_PATH} -u \
    && rm ${MINICONDA_INSTALL_FILE}

# Start the env and add channels and base dependencies
RUN . $MINICONDA_PATH/bin/activate && \
    conda config --add channels conda-forge && \
    conda install conda-build && \
    conda install ipython pyyaml numpy astropy ipyaladin astroML

USER ${SPTUSER}
WORKDIR ${SPTHOME}

#USER $SPTUSER
#WORKDIR /home/$SPTUSER

ENTRYPOINT ["/bin/bash", "-c","source /opt/startup.sh"]
