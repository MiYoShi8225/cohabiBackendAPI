
import boto3
from boto3.dynamodb.conditions import Key  # キーの取得

dynamodb = boto3.resource('dynamodb')  # AWSサービスのリソースタイプの宣言
table = dynamodb.Table("COHABI-USER-DATABASE")  # dynamoテーブル名


class Post_Request:
    pass

class Get_Request:
    pass

class Put_Request:
    pass

class Del_Request:
    pass
