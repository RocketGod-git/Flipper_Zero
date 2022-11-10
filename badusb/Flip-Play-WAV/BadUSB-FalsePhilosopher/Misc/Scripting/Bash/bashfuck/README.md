# BashFuck!

Original repo: https://github.com/0xddaa/bashfuck

BashFuck is an esoteric and educational programming style based on the atomic parts of Bash.
It uses only 11 different characters to write and execute code.

![BashFuck example](bashfuck.png)

The current charset used is: `$`, `(`, `)`, `#`, `!`, `{`, `}`, `<`, `\ `, `'`, `,`

```
usage: bashfuck.sh [-h] [-t] [-b] cmd

encode a bash command with charset $()#!{}<\',

positional arguments:
  cmd

optional arguments:
  -h, --help  show this help message and exit
  -t, --test  test bashfuck and output result
  -b, --bash  leaves the default bash string using [bash] chars, but avoids
              the usage of the "!" and uses one byte less. always works.
```
