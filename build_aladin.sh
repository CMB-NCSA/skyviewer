#!/bin/bash

set -e

if [[ ! -d "aladin-lite" ]]; then
    echo "You must first clone the aladin-lite repo as instructed in the README.md file."
    exit 1
fi

docker run --rm -it -p 8088:8088 \
    -v $(pwd)/aladin-lite:/home/node/src \
    registry.gitlab.com/cmb-ncsa/aladin-lite \
    npm run build

cp aladin-lite/dist/aladin.umd.cjs www/js/

echo "Open \`www/index.html\` in a browser or serve the \`www\` folder using a local webserver."
