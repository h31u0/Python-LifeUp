import requests

app_key = input('Enter app key: ')
app_secret = input('Enter app secret: ')

print("Open:", "https://www.dropbox.com/oauth2/authorize?client_id="+app_key+"&response_type=code&token_access_type=offline")

authorization_code = input('Enter authorization code: ')

params = {
    "code": authorization_code,
    "grant_type": "authorization_code",
    "client_id": app_key,
    "client_secret": app_secret
}
r = requests.post("https://api.dropboxapi.com/oauth2/token", data=params)
print(r.text)
