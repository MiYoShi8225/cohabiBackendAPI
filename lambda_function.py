import json
from comm_env.CommonFunction import Return_Msg
from prod_env import HttpRequestFunction
from prod_env.DynamoDBAccessFunciton import Dynamo_Access

"""test data function"""


def lambda_handler(event, context):
    try:
        routekey_split = []
        print("##lambda_handler start")

        print("##event info:\n{}\n".format(event))
        http_req = HttpRequestFunction.Http_Request(event)
        dynamo_acs = []
        dynamo_acs = Dynamo_Access(
            http_req.request, http_req.route, http_req.body, http_req.query_GroupID(
            ), http_req.query_DataID(), http_req.userid, http_req.query_datesort()
        )
        
        message = "##success:request:{} route:{}".format(http_req.request, http_req.route)
        return Return_Msg.return_successJson(message, dynamo_acs.return_result())
        print("##lambda_handler end")

    except Exception as e:
        print("##lambda_handler Error")
        return Return_Msg.return_errorJson(e)
