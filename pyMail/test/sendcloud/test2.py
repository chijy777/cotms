import json

r = {"result":'true',"statusCode":200,"message":"请求成功","info":{"emailIdList":["1530854126308_100993_12909_8060.sc-10_9_63_161-inbound0$2585747805@qq.com"]}}

json_str = json.dumps(r)

data = json.loads(json_str)
print(data)
print(data['result'])
print(data['statusCode'])
print(data['message'])
print(data['info'])
