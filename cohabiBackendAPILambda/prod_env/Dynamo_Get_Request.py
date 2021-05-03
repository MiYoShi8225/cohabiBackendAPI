
from logging import NullHandler
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名


class Get_Request:
    def __init__(self, group_id, date_sort, user_id):
        self.group_id = str(group_id)
        self.date_sort = date_sort
        self.user_id = user_id

    def costs(self):
        bodyItems = []
        GroupID = "COSTS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(
                GroupID) & Key("DATA_TYPE").begins_with(self.date_sort)
        )

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            # tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]
            bodyItems.append({
                "date": date_reverce_proc,
                "id": f["DATA_TYPE"],
                "value": f["DATA_VALUE"],
                "user": f["USER"],
                "category": f["CATEGORY"],
                "comment": f["COMMENT"]
            })

        return bodyItems

    def categories(self):
        bodyItems = []
        GroupID = "CATEGORIES_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").begins_with("No"))
            
        Date = "No_" + datetime.datetime.now().strftime('20%y%m%d%H%M%S%f')
        
        if len(dynamoData["Items"]) == 0:
        
            # categoriesの情報がない場合の処理(初期情報を扱う)
            putResponse = table.put_item(
                Item={
                    'ID': GroupID,
                    'DATA_TYPE': Date,
                    'DATA_VALUE': 'default category',
                    'TIMESTAMP': datetime.datetime.now().strftime('20%y%m%d%H%M%S%f'),
                    'DISABLED': False
                }
            )
            
            dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").begins_with("No"))
        
        for f in dynamoData["Items"]:
            bodyItems.append({
                "id": f["DATA_TYPE"],
                "index": int(f["DATA_TYPE"].split('_')[1]),
                "name": f["DATA_VALUE"],
                "disabled": f["DISABLED"]
            })
        
        return bodyItems

    def todos(self):
        bodyItems = []
        GroupID = "TODOS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))

        for f in dynamoData["Items"]:
            #tmp = f["DATA_TYPE"].split('_')[0]

            if f["STATUS"] == "done":
                STATUS = True
            else:
                STATUS = False

            bodyItems.append({
                "id": f["DATA_TYPE"],
                "name": f["DATA_VALUE"],
                "comment": f["COMMENT"],
                "done": STATUS
            })

        return bodyItems

    def calendars(self):
        bodyItems = []
        GroupID = "CALENDARS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            # tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]

            bodyItems.append({
                "id": f["DATA_TYPE"],
                "date": date_reverce_proc,
                "name": f["DATA_VALUE"],
                "comment": f["COMMENT"],
                "user": f["USER"]
            })

        return bodyItems

    def me(self):
        bodyItems = {}
        UserID = "USERS_" + self.user_id
        Groupdata = []
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(UserID))
        
        for f in dynamoData["Items"]:
            if f["DATA_TYPE"] == "userdata":
                bodyItems.update(f["DATA_VALUE"])

            if f["DATA_TYPE"] == "groups":
                for group in f["DATA_VALUE"]:
                    GroupID = "GROUPS_" + group
                    dynamoData2 = table.query(
                        KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").eq("groupdata"))
                    
                    print(dynamoData2["Items"][0]["DATA_VALUE"]["name"])
                    Groupdata.append({
                        "id": group,
                        "name": dynamoData2["Items"][0]["DATA_VALUE"]["name"]
                    })
                    
            bodyItems.update({
                    "id": self.user_id,
                    "groups": Groupdata
            })
        
        return bodyItems

    def groups(self):
        bodyItems = {}
        Name = None
        Users = []
        GroupID = "GROUPS_" + self.group_id

        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))
        
        for f in dynamoData["Items"]:
            if f["DATA_TYPE"] == "groupdata":
                Name = f['DATA_VALUE']
            if f["DATA_TYPE"] == "users":
                Users = f['DATA_VALUE']
        
        Users_data = []

        for User in Users:
            UserID = "USERS_" + User
            dynamoData3 = table.query(
            KeyConditionExpression=Key("ID").eq(UserID))

            name = None
            for f in dynamoData3["Items"]:
                if f["DATA_TYPE"] == "userdata":
                    name = f["DATA_VALUE"]["name"]
            
            Users_data.append({
                "id": User,
                "name": name
            })

        bodyItems.update({
            "id": self.group_id,
            "name": Name,
            "users": Users_data
        })

        return bodyItems
