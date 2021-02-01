# file name: cohabiMePost.py
#    author: miyoshi
#      date: 2020/11/12
#    update:

class Http_Request:
    def __init__(self, event_param):
        self.event_param = event_param

    def ttt(self):
        self.routekey_split = []

        self.routekey_split = self.event_param["routeKey"].split(" ")
        
        #httpのリクエスト
        self.request = self.routekey_split[0]

        #httpのルート
        self.route = self.routekey_split[1]

    #共通GroupID取得関数
    def __init__(self):
        self.query_param = self.event_param["queryStringParameters"]

    def query_GroupID(self):
        params = self.query_param["g"]
        return params

    #queryにきた”id”を加工して返す
    def query_DataID(self):
        params = self.query_param["id"]
        return params