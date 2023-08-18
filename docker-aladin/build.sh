export IMAGE=registry.gitlab.com/cmb-ncsa/aladin-lite
export TAG=v3.2.0
echo "will run: "
echo "docker build -t $IMAGE:$TAG ."
docker build -t $IMAGE:$TAG .

echo "Ready: $IMAGE:$TAG"
