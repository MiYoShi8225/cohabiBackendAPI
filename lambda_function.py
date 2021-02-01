import json
from comm_env.CommonFunction import Error_Msg
from prod_env import HttpRequestFunction
from prod_env.DynamoDBAccessFunciton import Dynamo_Access

"""test data function"""
from test_env import signup_test

"""test data function"""


def lambda_handler(event, context):
    try:
        routekey_split = []
        print("##lambda_handler start")

        print("event info:{}".format(event))
        http_req = HttpRequestFunction.Http_Request(event)
        dynamo_acs = Dynamo_Access(http_req.request, http_req.route, http_req.body)
        
        print("##lambda_handler end")

    except Exception as e:
        print("##lambda_handler Error")
        return Error_Msg.return_errorJson(e)
