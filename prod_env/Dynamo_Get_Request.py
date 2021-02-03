
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名


class Get_Request:
    def __init__(self, group_id, date_sort):
        self.group_id = str(group_id)
        self.date_sort = date_sort
        self.bodyItems = []

    def costs_get(self):
        GroupID = "COSTS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(
                GroupID) & Key("DATA_TYPE").begins_with(self.date_sort)
        )

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            # tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]
            self.bodyItems.append({
                "date": date_reverce_proc,
                "id": f["DATA_TYPE"],
                "value": f["DATA_VALUE"],
                "user": f["USER"],
                "category": f["CATEGORY"],
                "comment": f["COMMENT"],
                "timestamp": f["TIMESTAMP"]
            })

        return self.bodyItems

    def categories_get(self):
        GroupID = "CATEGORIES_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID) & Key("DATA_TYPE").begins_with("No"))

        for f in dynamoData["Items"]:
            #tmp = f["DATA_TYPE"].split('_')[0]

            self.bodyItems.append({
                "id": f["DATA_TYPE"].split('_')[1],
                "name": f["DATA_VALUE"],
                "disabled": f["DISABLED"]
            })

        return self.bodyItems

    def todos_get(self):
        GroupID = "TODOS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(GroupID))

        for f in dynamoData["Items"]:
            #tmp = f["DATA_TYPE"].split('_')[0]

            if f["STATUS"] == "done":
                STATUS = True
            else:
                STATUS = False

            self.bodyItems.append({
                "id": f["DATA_TYPE"],
                "name": f["DATA_VALUE"],
                "comment": f["COMMENT"],
                "done": STATUS
            })

        return self.bodyItems
