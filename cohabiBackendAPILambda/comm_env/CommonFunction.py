
from datetime import date
import json #jsonのインポート
import datetime #date宣言のインポート

#return用class
class Return_Msg:
    #リターンjson形式
    def return_successJson(message, body):
        return_Json = {"result":{"error": False,"messages": str(message)}, "body":body} #bodyはリスト[]
        print("##success message:\n{}".format(message))
        return return_Json

    #共通エラー関数
    def return_errorJson(message):
        return_errorJson = {"result":{"error": True, "messages": str(message), "body": None}}
        print("##error message:\n{}".format(message))
        return return_errorJson
