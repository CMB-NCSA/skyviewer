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

## Copy source code
COPY --chown=node:node aladin-lite/ ./aladin-lite/
WORKDIR /home/node/aladin-lite

## Build JavaScript
RUN npm install
RUN npm run build

CMD ["npm", "run", "serve"]
