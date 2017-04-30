import os
import requests
import json

ACCESS_TOKEN_ENV = 'POPCLIP_OPTION_ACCESS_TOKEN'
GET_TOKEN_URL = 'https://api.shanbay.com/oauth2/authorize/?client_id=3afa2ca40713855221e0&response_type=token'

access_token = os.environ.get(ACCESS_TOKEN_ENV, '')
word = os.environ.get('POPCLIP_TEXT', '')

r = requests.get('https://api.shanbay.com/bdc/search/',
	params={'word': word}
)
r = r.json()

if r['status_code'] != 0:
	print(r['msg'])
	exit(0)
	
word_definition = r['data']['definition'].replace('\n', ' ')
	
word_id = r['data']['id']
r = requests.post('https://api.shanbay.com/bdc/learning/',
	headers={'Authorization': 'Bearer ' + access_token},
	data={'id': word_id}
)

if r.status_code == 401:
	print('AccessToken无效。请访问 {} 获取token，并在选项中填写。'.format(GET_TOKEN_URL))
	exit(0)
elif r.status_code == 429:
	print('API请求次数过多。请稍后再试。')
	exit(0)
elif r.status_code != 200:
	print('未知的HTTP状态码：{}'.format(r.status_code))
	exit(0)

r = r.json()
if r['status_code'] != 0:
	print('添加单词到词库时发生了业务错误。 {}: {}'.format(r['status_code'], r['msg']))
	exit(0)

print(word_definition)
