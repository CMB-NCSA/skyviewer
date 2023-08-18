export IMAGE=registry.gitlab.com/cmb-ncsa/aladin-lite
export ALADING_LITE_VERSION="v3.2.0"
export TAG=$ALADING_LITE_VERSION
echo "will run: "
echo "docker build -t $IMAGE:$TAG --build-arg $ALADING_LITE_VERSION ."
docker build -t $IMAGE:$TAG --build-arg ALADING_LITE_VERSION .

echo "Ready: $IMAGE:$TAG"
