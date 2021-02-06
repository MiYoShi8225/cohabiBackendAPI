
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
        self.bodyItems = {}
        self.user_id = user_id

    def costs(self):
        GroupID = "COSTS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(
                GroupID) & Key("DATA_TYPE").begins_with(self.date_sort)
        )

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            # tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]
            self.bodyItems.update({
                "date": date_reverce_proc,
                "id": f["DATA_TYPE"],
                "value": f["DATA_VALUE"],
                "user": f["USER"],
                "category": f["CATEGORY"],
                "comment": f["COMMENT"]
            })

        return self.bodyItems

    def categories(self):
        GroupID = "CATEGORIES_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").begins_with("No"))

        for f in dynamoData["Items"]:
            self.bodyItems.update({
                "id": f["DATA_TYPE"],
                "index": int(f["DATA_TYPE"].split('_')[1]),
                "name": f["DATA_VALUE"],
                "disabled": f["DISABLED"]
            })

        return self.bodyItems

    def todos(self):
        GroupID = "TODOS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))

        for f in dynamoData["Items"]:
            #tmp = f["DATA_TYPE"].split('_')[0]

            if f["STATUS"] == "done":
                STATUS = True
            else:
                STATUS = False

            self.bodyItems.update({
                "id": f["DATA_TYPE"],
                "name": f["DATA_VALUE"],
                "comment": f["COMMENT"],
                "done": STATUS
            })

        return self.bodyItems

    def calendars(self):
        GroupID = "CALENDARS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            # tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]

            self.bodyItems.update({
                "id": f["DATA_TYPE"],
                "date": date_reverce_proc,
                "name": f["DATA_VALUE"],
                "comment": f["COMMENT"],
                "user": f["USER"]
            })

        return self.bodyItems

    def me(self):
        UserID = "USERS_" + self.user_id
        Groupdata = []
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(UserID))
        
        for f in dynamoData["Items"]:
            if f["DATA_TYPE"] == "userdata":
                self.bodyItems.update(f["DATA_VALUE"])

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
                    
            self.bodyItems.update({
                    "id": self.user_id,
                    "groups": Groupdata
            })
        
        return self.bodyItems

    def groups(self):
        Name = None
        Users = []
        GroupID = "GROUPS_" + self.group_id
        """
        dynamoData1 = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").eq("name"))

        for f in dynamoData1["Items"]:
            Name = f['DATA_VALUE']

        dynamoData2 = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").eq("users"))
        
        for f in dynamoData2["Items"]:
            Users = f['DATA_VALUE']
        """

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

        self.bodyItems.update({
            "id": self.group_id,
            "name": Name,
            "users": Users_data
        })

        return self.bodyItems
