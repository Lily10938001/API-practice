from marshmallow import Schema, fields

#Schema  #設計parameter底下的功能
class UserGetSchema(Schema):   #新增可以填寫parameter做查詢(get)的功能
    name = fields.Str(example="string")   #填寫的欄位為"name"

class UserPostSchema(Schema):  #新增可以填寫parameter做提交(post)的功能
    name = fields.Str(doc="name", example="string", required=True)   #填寫的欄位為"name"且必填
    gender = fields.Str(doc="gender", example="string", required=True)
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)
    birth = fields.Str(doc="birth", example="string")
    note = fields.Str(doc="note", example="string")
 
class UserPatchSchema(Schema):  #新增可以填寫parameter做提交(post)並修改的功能
    name = fields.Str(doc="name", example="string")
    gender = fields.Str(doc="gender", example="string")
    account = fields.Str(doc="account", example="string")
    password = fields.Str(doc="password", example="string")
    birth = fields.Str(doc="birth", example="string")
    note = fields.Str(doc="note", example="string")

class LoginSchema(Schema):   #新增可以填寫parameter做login的功能
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)

# Response
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())

class UserCommonResponse(Schema):
    message = fields.Str(example="success")