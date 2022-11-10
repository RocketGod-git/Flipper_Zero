    REM Author: Cody Theodore
    REM Title: OSX Youtube Blast
    REM This payload will open terminal, crank up the Macs volume all the way, then open a youtube video of
    REM your choice by replacing the link.
    DELAY 1000
    GUI SPACE
    STRING terminal
    DELAY 500
    RETURN
    DELAY 4000
    STRING osascript -e 'set volume 7'
    DELAY 500
    RETURN
    DELAY 500
    STRING open https://www.youtube.com/watch?v=dQw4w9WgXcQ
    DELAY 500
    RETURN