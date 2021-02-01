# file name: cohabiLambdaCommon.py
#    author: miyoshi
#      date: 2020/11/04
#    update:

from datetime import date
import json #jsonのインポート
import datetime #date宣言のインポート

#return用class
class Return_Msg:
    #リターンjson形式
    def return_successJson(message, body):
        return_Json = {"result":{"error": False,"messages": str(message)}, "body":body} #bodyはリスト[]
        print(message)
        return return_Json

    #共通エラー関数
    def return_errorJson(message):
        return_errorJson = {"result":{"error": True, "messages": str(message), "body": None}}
        print(message)
        return return_errorJson

#データ整理用class
class Data_Format:
    """
    def body_data(event_param):
        json.loads(event_param['body']) #bodyに入っている値を代入


    #inputparamのbodyに来た日付情報をyyyyMMddに変更する
    def date_Proc(event_param):
        inputparam = json.loads(event_param['body'])
        date_Proc = inputparam['date'].split('/')[0] + inputparam['date'].split('/')[1] + inputparam['date'].split('/')[2]
        return date_Proc
    

    #paramよりyyyy/MM形式の情報を取得する
    def query_DateSortKey(event_param):
        params = event_param["pathParameters"]    
        dateSort =[params['yyyy'], params['MM']]
        return dateSort

    
    #JSONの表示をfloat型に対応するための関数
    def decimal_default_proc(obj):
        from decimal import Decimal
        if isinstance(obj, Decimal):
            #return float(obj)
            return int(obj)
        raise TypeError

    #JSONで返す値を整形する関数
    def return_Json_Dumps(returnJson):
        jsonDumps = json.dumps(returnJson,indent = 2, ensure_ascii = False, default=decimal_default_proc)
        return jsonDumps
    

    #userIDの取得
    def userID(event_param):
        userID = event_param["requestContext"]["authorizer"]["jwt"]["claims"]["cognito:user"]
        return userID
    """

    #yyyyMMddHHmmssffでタイムスタンプを返す関数
    def timeStump():
        dt=datetime.datetime.now()
        dt_now=dt.strftime('20%y%m%d%H%M%S%f')
        return dt_now
