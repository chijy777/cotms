from urllib import request
from urllib import request, parse

url = "http://127.0.0.1:8801/ontkyc/notify"

print('Test client post...')

username = input('Username: ')
passwd = input('Password: ')
login_data = parse.urlencode([
    ('username', username),
    ('password', passwd),
])

req = request.Request(url)

with request.urlopen(req, data=login_data.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
