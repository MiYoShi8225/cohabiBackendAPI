
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名
#table = dynamodb.Table("accounting-book") #旧dynamoテーブル

class Dynamo_Access:
    def __init__(self, request, route, body, group_id, data_id, userid, date_sort):
        self.exe_result = []
        #self.exe_result["message"] = "##success: request:{} route:{}".format(request, route)

        if request == "POST":
            post_req = Post_Request(body, group_id, data_id, userid)
            if route == "/costs":
                post_req.costs_post()
        elif request == "GET":
            get_req = Get_Request(group_id, date_sort)
            if route == "/costs/{yyyy}/{MM}":
                self.exe_result.append(get_req.costs_get())
        elif request == "PUT":
            pass
        elif request == "DELETE":
            pass

    def return_result(self):
        return self.exe_result


class Post_Request:
    def __init__(self, body, group_id, data_id, userid):
        self.body = json.loads(body)
        self.group_id = str(group_id)
        self.data_id = data_id
        self.user_id = userid

    def costs_post(self):
        Value = self.body['value']
        Category = self.body['category']
        Comment = self.body['comment']
        GroupID = "COSTS_" + self.group_id
        Date = self.body['date'].split('/')[0] + self.body['date'].split('/')[
            1] + self.body['date'].split('/')[2] + "_" + datetime.datetime.now().strftime('%H%M%S%f')

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Date,
                'DATA_VALUE': Value,
                'TIMESTAMP': datetime.datetime.now().strftime('20%y%m%d%H%M%S%f'),
                'COMMENT': Comment,
                'CATEGORY': Category,
                'USER': self.user_id
            }
        )

        print(putResponse)


class Get_Request:
    def __init__(self, group_id, date_sort):
        self.group_id = str(group_id)
        self.date_sort = date_sort

    def costs_get(self):
        GroupID = "COSTS_" + self.group_id
        dynamoData = table.query(
            KeyConditionExpression=Key("ID").eq(
                GroupID) & Key("DATA_TYPE").begins_with(self.date_sort)
        )
        
        bodyItems=[]

        for f in dynamoData["Items"]:
            tmp = f["DATA_TYPE"].split('_')[0]
            #tmp[:4]はスタート0配列目から4ステップまで、tmp[4:6]は4配列目から6ステップまで、tmp[6:]はエンドから6配列目まで
            date_reverce_proc = tmp[:4] + "/" + tmp[4:6] + "/" + tmp[6:]
            bodyItems.append({
                "date": date_reverce_proc,
                "id": f["DATA_TYPE"],
                "value": f["DATA_VALUE"],
                "user": f["USER"],
                "category": f["CATEGORY"],
                "comment": f["COMMENT"],
                "timestamp": f["TIMESTAMP"]
            })
        
        return bodyItems


class Put_Request:
    pass


class Del_Request:
    pass
