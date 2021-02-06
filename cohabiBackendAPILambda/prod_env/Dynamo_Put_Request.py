
from types import SimpleNamespace
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

    def me(self):
        UserID = "USERS_" + self.user_id
        Data_type = "userdata"
        Name = self.body["name"]
        email = self.body["email"]

        putResponse = table.put_item(
            Item={
                'ID': UserID,
                'DATA_TYPE': Data_type,
                'DATA_VALUE': {
                    "name": Name,
                    "email": email
                }
            }
        )

        print(putResponse)

    def groups(self):
        GroupID = "GROUPS_" + self.group_id
        add_users = []
        remove_users = []

        if "name" in self.body:
            Name = self.body['name']
            putResponse = table.put_item(
                Item={
                    'ID': GroupID,
                    'DATA_TYPE': "groupdata",
                    'DATA_VALUE': {
                        "name": Name
                    }
                }
            )
            print(putResponse)

        if "add_user" in self.body:
            add_users = self.body['add_user']
        if "remove_user" in self.body:
            remove_users = self.body['remove_user']

        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").eq("users"))

        Users = []

        for f in dynamoData["Items"]:
            Users.extend(f['DATA_VALUE'])

        if len(add_users) == 0 & len(remove_users) == 0:
            return

        # user追加
        if len(add_users) != 0:
            Users.extend(add_users)
            for user in add_users:
                userID = "USERS_" + user
                dynamoData = table.query(
                    KeyConditionExpression=Key("ID").eq(userID) & Key("DATA_TYPE").eq("groups"))

                groups = []
                groups.extend(dynamoData["Items"][0]["DATA_VALUE"])
                groups.append(self.group_id)

                putResponse = table.put_item(
                    Item={
                        'ID': userID,
                        'DATA_TYPE': "groups",
                        'DATA_VALUE': groups
                    }
                )

        # user削除
        if len(remove_users) != 0:
            for remove_user in remove_users:
                Users.remove(remove_user)
                for user in add_users:
                    userID = "USERS_" + user
                    dynamoData = table.query(
                        KeyConditionExpression=Key("ID").eq(userID) & Key("DATA_TYPE").eq("groups"))

                    groups = []
                    groups.extend(dynamoData["Items"][0]["DATA_VALUE"])
                    groups.remove(self.group_id)

                    putResponse = table.put_item(
                        Item={
                            'ID': userID,
                            'DATA_TYPE': "groups",
                            'DATA_VALUE': groups
                        }
                    )

        putResponse2 = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': "users",
                'DATA_VALUE': Users
            }
        )

        print(putResponse2)
