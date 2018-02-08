const_value ={
    'TTL' : 500000,
    'TOKEN_DOES_NOT_EXIST' : 'token does not exist',
}

status_code = {
    'LOGIN_SUCCESS' : {
        'code' : 1100,
        'msg' : 'Login successed',
        'option' :
    }

}


from common.const import const_value, status_code

Response({'result' : status_code['LOGIN_SUCCESS']},status=status.HTTP_200_OK)