
from logging import disable
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得
import datetime  # date宣言のインポート
import json
from prod_env.Dynamo_Post_Request import Post_Request
from prod_env.Dynamo_Get_Request import Get_Request
from prod_env.Dynamo_Put_Request import Put_Request
from prod_env.Dynamo_Del_Request import Del_Request


class Dynamo_Access:
    def __init__(self, request, route, body, group_id, data_id, userid, date_sort):
        self.exe_result = []
        if request == "POST":
            post_req = Post_Request(body, group_id, data_id, userid)

            if route == "/costs":
                post_req.costs()
            if route == "/categories":
                post_req.categories()
            if route == "/todos":
                post_req.todos()
            if route == "/calendars":
                post_req.calendars()

        elif request == "GET":
            get_req = Get_Request(group_id, date_sort)

            if route == "/costs/{yyyy}/{MM}":
                self.exe_result.append(get_req.costs())
            if route == "/categories":
                self.exe_result.append(get_req.categories())
            if route == "/todos":
                self.exe_result.append(get_req.todos())
            if route == "/calendars":
                self.exe_result.append(get_req.calendars())

        elif request == "PUT":
            put_req = Put_Request(body, group_id, data_id, userid)

            if route == "/costs":
                put_req.costs()
            if route == "/todos":
                put_req.todos()
            if route == "/calendars":
                put_req.calendars()

        elif request == "DELETE":
            put_req = Del_Request(group_id, data_id)

            if route == "/costs":
                put_req.costs()
            if route == "/todos":
                put_req.todos()
            if route == "/calendars":
                put_req.calendars()

    def return_result(self):
        return self.exe_result

