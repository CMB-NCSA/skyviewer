FROM jupyter/scipy-notebook:2023-04-10

USER root
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

USER $NB_UID
WORKDIR $HOME

RUN mamba install --yes \
    'ipython'  \
    'pyyaml' \
    'numpy' \
    'astropy' \
    'ipyaladin' \
    'astroML' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
