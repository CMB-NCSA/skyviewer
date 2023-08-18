FROM node:18

ARG UID=${UID:-1000}
ARG GID=${GID:-1000}
RUN groupmod -g ${GID} node && usermod -u ${UID} -g ${GID} node

RUN apt-get update && DEBIAN_FRONTEND=noninteractive && apt-get install -y \
    xdg-utils \
    && rm -rf /var/lib/apt/list/*

USER node
WORKDIR /home/node

## Install build toolchain dependencies
##
## Install Rust toolchain installer (https://rustup.rs/)
RUN sh -c 'curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s - -y'
ENV PATH="/home/node/.cargo/bin:$PATH"
## Install wasm-pack (https://rustwasm.github.io/wasm-pack/)
RUN sh -c 'curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh'

# Get the source code
RUN git clone -b main https://github.com/CMB-NCSA/aladin-lite.git
RUN mv -v aladin-lite aladin-lite-docker

WORKDIR /home/node/aladin-lite-docker

# Build JavaScript
RUN npm install
RUN npm run build

CMD ["npm", "run", "serve"]
