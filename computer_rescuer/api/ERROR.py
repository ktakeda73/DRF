SYS_ERR = 'システムエラーが発生しました'
AUTH_ERR = '{*1}{*2}権限がありません'
USER_EXIST_ERR = 'ユーザーは既に存在します'
BODY_ERR = 'IDおよびユーザーIDは変更できません'
FIELD_ERR = '存在しないカラムを指定しています'
def getErrorMsg(msg, args):
    for k, v in args.items():
        arg = '{*' + str(k) + '}'
        msg = msg.replace(arg, v)
    
    return msg
    
    