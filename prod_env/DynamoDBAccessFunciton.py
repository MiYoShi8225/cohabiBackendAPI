
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名

class Dynamo_Access:
    def __init__(self, request, route, body):
        self.request = request
        self.route = route
        self.body = body

        if self.request == "POST":
            Post_Request(self.route, self.body)
        elif self.request == "PUT":
            pass
        elif self.request == "GET":
            pass
        elif self.request == "DELETE":
            pass

class Post_Request:
    def __init__(self, route, body):
        route
        self.body = body
        if route == "/cost":
            Post_Request.cost_post()

    def cost_post(self):
        Value = self.body['value']
        Category = self.body['category']
        Comment = self.body['comment']

        putResponse = table.post_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Date,
                'DATA_VALUE': Value,
                'TIMESTAMP': cohabiLambdaCommon.timeStump(),
                'COMMENT': Comment,
                'CATEGORY': Category,
                'USER': UserID
            }
        )
        print(putResponse)

        #json形式に変換
        #returnJson = cohabiLambdaCommon.return_Json_Dumps(returnJson)


class Get_Request:
    pass

class Put_Request:
    pass

class Del_Request:
    pass
