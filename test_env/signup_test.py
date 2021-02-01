
import lambda_function


print("###signup_test start")

event = {'version': '2.0', 'routeKey': 'POST /signup', 'rawPath': '/signup', 'rawQueryString': 'mode=signup', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ja-jp', 'cache-control': 'max-age=0', 'content-length': '47', 'content-type': 'application/json; charset=utf-8', 'host': 'kakeibo-api.unison-8225.com', 'origin': 'https://kakeibo.unison-8225.com', 'referer': 'https://kakeibo.unison-8225.com/signup', 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1', 'x-amzn-trace-id': 'Root=1-5f9e4ccb-5a8681cc470485dd67b8457e', 'x-forwarded-for': '221.241.4.240', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'queryStringParameters': {'mode': 'signup', 'g':'test'}, 'requestContext': {'accountId': '515341273341', 'apiId': 'bpvhlmtisc', 'domainName': 'kakeibo-api.unison-8225.com', 'domainPrefix': 'kakeibo-api', 'http': {'method': 'POST', 'path': '/signup', 'protocol': 'HTTP/1.1', 'sourceIp': '221.241.4.240', 'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1'}, 'requestId': 'VUDvxj1pNjMEPQg=', 'routeKey': 'POST /signup', 'stage': '$default', 'time': '01/Nov/2020:05:51:07 +0000', 'timeEpoch': 1604209867244}, 'body': '{"userName":"kkkk","email":"kzyk404@gmail.com"}', 'isBase64Encoded': False}
context = "<__main__.LambdaContext object at 0x7fa5d37bfdf0>"

lambda_function.lambda_handler(event, context)