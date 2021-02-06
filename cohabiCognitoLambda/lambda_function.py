
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名


def lambda_handler(event, context):
    try:
        print("##lambda_handler start")

        print("##event info:\n{}\n".format(event))

        userName = event["userName"]
        email = event["request"]["userAttributes"]["email"]
        sub = event["request"]["userAttributes"]["sub"]

        userID = "USERS_" + userName

        #userの情報をDynamoに追加
        putResponse = table.put_item(
            Item={
                'ID': userID,
                'DATA_TYPE': "userdata",
                'DATA_VALUE': {
                    'name': userName,
                    'email': email,
                    'sub': sub
                }
            }
        )
        print(putResponse)

        #userのdefaultグループをDynamoに追加
        putResponse = table.put_item(
            Item={
                'ID': userID,
                'DATA_TYPE': "groups",
                'DATA_VALUE': [
                    userName
                ]
            }
        )
        print(putResponse)

        GroupID = "GROUPS_" + userName

        #defaultグループをDynamoに追加
        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': "groupdata",
                'DATA_VALUE': {
                    'name': 'defaultGroup'
                }
            }
        )
        print(putResponse)

        #defaultグループにuserを追加
        putResponse = table.put_item(
            Item={
                'ID': GroupID,
                'DATA_TYPE': "users",
                'DATA_VALUE': [
                    userName
                ]
            }
        )
        print(putResponse)

        #cognitoはeventをreturnで返す必要あり
        return event

    except Exception as e:
        print("##lambda_handler Error")
        print(e)

        return e
