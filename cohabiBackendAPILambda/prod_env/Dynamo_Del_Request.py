

import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名

class Del_Request:
    def __init__(self, group_id, data_id):
        self.group_id = str(group_id)
        self.data_id = data_id

    def costs(self):
        GroupID = "COSTS_" + self.group_id
        putResponse = table.delete_item(
            Key={
                'ID': GroupID,
                'DATA_TYPE': self.data_id,
            }
        )
        print("##delete dynamo data.")
        print(putResponse)

    def todos(self):
        GroupID = "TODOS_" + self.group_id
        putResponse = table.delete_item(
            Key={
                'ID': GroupID,
                'DATA_TYPE': self.data_id,
            }
        )
        print("##delete dynamo data.")
        print(putResponse)
    
    def calendars(self):
        GroupID = "CALENDARS_" + self.group_id
        putResponse = table.delete_item(
            Key={
                'ID': GroupID,
                'DATA_TYPE': self.data_id,
            }
        )
        print("##delete dynamo data.")
        print(putResponse)
    