export IMAGE=skyviewer_aladin
export SPTUSER=$USER

export TAG=test
docker build -f ./Dockerfile -t menanteau/$IMAGE:$TAG --build-arg SPTUSER --rm=true .
