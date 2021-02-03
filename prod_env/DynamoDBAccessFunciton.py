
from logging import disable
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名


class Dynamo_Access:
    def __init__(self, request, route, body, group_id, data_id, userid, date_sort):
        self.exe_result = []
        if request == "POST":
            post_req = Post_Request(body, group_id, data_id, userid)

            if route == "/costs":
                post_req.costs_post()
            if route == "/categories":
                post_req.categories_post()
            if route == "/todos":
                post_req.todos_post()

        elif request == "GET":
            get_req = Get_Request(group_id, date_sort)

            if route == "/costs/{yyyy}/{MM}":
                self.exe_result.append(get_req.costs_get())
            if route == "/categories":
                self.exe_result.append(get_req.categories_get())
            if route == "/todos":
                self.exe_result.append(get_req.todos_get())

        elif request == "PUT":
            put_req = Put_Request(body, group_id, data_id, userid)

            if route == "/costs":
                put_req.costs_put()
            if route == "/todos":
                put_req.todos_put()

        elif request == "DELETE":
            put_req = Del_Request(group_id, data_id)

            if route == "/costs":
                put_req.costs_del()
            if route == "/todos":
                put_req.todos_del()

    def return_result(self):
        return self.exe_result


class Post_Request:
    def __init__(self, body, group_id, data_id, userid):
        self.body = json.loads(body)
        self.group_id = str(group_id)
        self.data_id = data_id
        self.user_id = userid
        self.date_now = datetime.datetime.now()

    def costs_post(self):
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

    def categories_post(self):
        GroupID = "CATEGORIES_" + self.group_id
        Date = "No_" + str(self.body['id'])
        Value = self.body['name']
        Disabled = self.body['disabled']

        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': Date,
                'DATA_VALUE': Value,
                'TIMESTAMP': self.date_now.strftime('20%y%m%d%H%M%S%f'),
                'DISABLED': Disabled
            }
        )

        print(putResponse)

    def todos_post(self):
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


class Del_Request:
    def __init__(self, group_id, data_id):
        self.group_id = str(group_id)
        self.data_id = data_id

    def costs_del(self):
        GroupID = "COSTS_" + self.group_id
        putResponse = table.delete_item(
            Key={
                'ID': GroupID,
                'DATA_TYPE': self.data_id,
            }
        )
        print("##delete dynamo data.")
        print(putResponse)

    def todos_del(self):
        GroupID = "TODOS_" + self.group_id
        putResponse = table.delete_item(
            Key={
                'ID': GroupID,
                'DATA_TYPE': self.data_id,
            }
        )
        print("##delete dynamo data.")
        print(putResponse)
