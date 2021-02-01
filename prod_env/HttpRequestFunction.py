# file name: cohabiMePost.py
#    author: miyoshi
#      date: 2020/11/12
#    update:

class Http_Request:
    def __init__(self, event_param):
        self.event_param = event_param

        #query関係の値を予め代入する(query_GroupID、query_DataIDで使用)
        self.query_param = self.event_param["queryStringParameters"]

        #body格納
        self.body = event_param["body"]

        #routekey に入っている情報を分解する
        self.routekey_split = []
        self.routekey_split = self.event_param["routeKey"].split(" ")
        #httpのリクエスト
        self.request = self.routekey_split[0]
        #httpのルート
        self.route = self.routekey_split[1]

    def query_GroupID(self):
        params = self.query_param["g"]
        return params

    #queryにきた”id”を加工して返す
    def query_DataID(self):
        params = self.query_param["id"]
        return params