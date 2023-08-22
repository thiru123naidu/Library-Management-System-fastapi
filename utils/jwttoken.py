
import jwt
import constant

def jenerate_jwt_token(payload):
    
    token=jwt.encode(payload,constant.JWT_SECRATE_PASSWORD,algorithm="HS256")

    return token


def decode_jwt_token(token):
    result = None
    try:
        result=jwt.decode(token,constant.JWT_SECRATE_PASSWORD,algorithms=["HS256"])
    except:
        print("invalid json token")
    return result




