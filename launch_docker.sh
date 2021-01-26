docker stop maskrcnn_dk
docker create -it \
    --gpus all \
    --runtime=nvidia --rm -it \
    --env="DISPLAY" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged \
    -v /etc/timezone:/etc/timezone:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v ~/dev:/root/dev \
    --network host \
    -w '/root/dev/' \
    --name=maskrcnn \
    maskrcnn_dk \
    && export containerId=$(docker ps -l -q) \
    && xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId` \
    && docker start $containerId

# docker exec -it maskrcnn_dk bash