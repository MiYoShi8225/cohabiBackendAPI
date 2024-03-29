
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名

class Post_Request:
    def __init__(self, body, group_id, data_id, userid):
        self.body = json.loads(body)
        self.group_id = str(group_id)
        self.data_id = data_id
        self.user_id = userid
        self.date_now = datetime.datetime.now()

    def costs(self):
        Value = self.body['value']
        Category = self.body['category']
        Comment = self.body['comment']
        GroupID = "COSTS_" + self.group_id
        self.date = self.body['date'].split(
            '/')[0] + self.body['date'].split('/')[1] + self.body['date'].split('/')[2]
        Date = self.date + "_" + self.date_now.strftime('%H%M%S%f')

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Date,
                'DATA_VALUE': Value,
                'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                'COMMENT': Comment,
                'CATEGORY': Category,
                'USER': self.user_id
            }
        )

        print(putResponse)

    def categories(self):
        GroupID = "CATEGORIES_" + self.group_id
        
        for index_no, body_info in enumerate(self.body):
            print(index_no)
            if body_info['id'] == "" :
                Date = "No_" + str(self.date_now.strftime('20%y%m%d%H%M%S%f'))
            else:
                Date = str(body_info['id'])
            Value = body_info['name']
            Disabled = body_info['disabled']
    
            putResponse = table.put_item(
                Item={
                    'ID': GroupID,
                    'DATA_TYPE': Date,
                    'DATA_VALUE': Value,
                    'INDEX': index_no,
                    'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                    'DISABLED': Disabled
                }
            )
    
            print(putResponse)

    def todos(self):
        Comment = self.body['comment']
        GroupID = "TODOS_" + self.group_id
        Value = self.body['name']

        if self.body['done'] == True:
            Status = "done"
        else:
            Status = "yet"

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': self.date_now.strftime('20%y%m%d_%H%M%S%f'),
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
        self.date = self.body['date'].split(
            '/')[0] + self.body['date'].split('/')[1] + self.body['date'].split('/')[2]
        Date = self.date + "_" + self.date_now.strftime('%H%M%S%f')
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
        Name = self.body['name']
        group_id = self.date_now.strftime('20%y%m%d%H%M%S%f')
        GroupID = "GROUPS_" + group_id

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
        
        Users = [self.user_id]
        putResponse2 = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': "users",
                'DATA_VALUE': Users
            }
        )

        print(putResponse2)

        userID = "USERS_" + self.user_id

        dynamoData = table.query(
                    KeyConditionExpression=Key("ID").eq(userID) & Key("DATA_TYPE").eq("groups"))

        groups = []
        groups.extend(dynamoData["Items"][0]["DATA_VALUE"])
        groups.append(str(group_id))

        putResponse3 = table.put_item(
            Item={
                'ID': userID,
                'DATA_TYPE': "groups",
                'DATA_VALUE': groups
            }
        )

        print(putResponse3)

