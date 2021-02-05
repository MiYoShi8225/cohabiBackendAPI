
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

    def costs(self):
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

    def todos(self):
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

    def calendars(self):
        GroupID = "CALENDARS_" + self.group_id
        Value = self.body['name']
        Date = self.data_id
        Comment = self.body['comment']

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Date,
                'DATA_VALUE': Value,
                'COMMENT': Comment,
                'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                'USER': self.user_id
            }
        )

        print(putResponse)

    def groups(self):
        GroupID = "GROUPS_" + self.group_id
        Name = self.body['name']
        add_users = self.body['add_user']
        remove_users = self.body['remove_user']

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': "name",
                'DATA_VALUE': Name
            }
        )

        print(putResponse)

        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").eq("users"))

        Users = []
        for f in dynamoData["Items"]:
            Users = f['DATA_VALUE']

        if add_users.len() == 0 & remove_users.len() == 0:
            return

        """
        闇するぎるグループにユーザーを追加するする処理(めっちゃ保留中)
        if add_users.len() != 0:
            Users.extend(add_users)
        """

        if remove_users.len() != 0:
            for remove_user in remove_users:
                Users.remove(remove_user)

            putResponse2 = table.put_item(
                Item={
                    'ID': GroupID,
                    'DATA_TYPE': "users",
                    'DATA_VALUE': Users
                }
            )

            print(putResponse2)
