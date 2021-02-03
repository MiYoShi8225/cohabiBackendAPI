
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名

class Put_Request:
    def __init__(self, body, group_id, data_id, userid):
        self.body = json.loads(body)
        self.date_now = datetime.datetime.now()
        self.group_id = str(group_id)
        self.data_id = data_id
        self.user_id = userid

    def costs_put(self):
        Value = self.body['value']
        Category = self.body['category']
        Comment = self.body['comment']
        GroupID = "COSTS_" + self.group_id
        Data = self.data_id

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Data,
                'DATA_VALUE': Value,
                'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                'COMMENT': Comment,
                'CATEGORY': Category,
                'USER': self.user_id
            }
        )
        print(putResponse)

    def todos_put(self):
        Comment = self.body['comment']
        GroupID = "TODOS_" + self.group_id
        Value = self.body['name']
        Data = self.data_id

        if self.body['done'] == True:
            Status = "done"
        else:
            Status = "yet"

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Data,
                'DATA_VALUE': Value,
                'COMMENT': Comment,
                'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                'STATUS': Status
            }
        )

        print(putResponse)