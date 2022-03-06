import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from . import user_swagger_model, util  #"."代表同一層
from flask_jwt_extended import create_access_token, jwt_required  #設定login元件的東東
from datetime import timedelta

# 連上sql
def db_init():
   db = pymysql.connect(
       host='127.0.0.1',
       user='root',
       password='root',
       port=3306,
       db='test'
   )
   cursor = db.cursor(pymysql.cursors.DictCursor)
   return db, cursor
 
def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

# 定義api功能
class Users(MethodResource):   #繼承MethodResource的class功能
   # Get user data
   @doc(description="Get user data", tags=["User"])  #在swagger網頁的"Users"標籤底下產生GET的區塊,並增添敘述
   @use_kwargs(user_swagger_model.UserGetSchema, location="query")  #新增可以填寫parameter做查詢的功能(文字引用我們所寫的user_swagger_model.py檔)
   @marshal_with(user_swagger_model.UserGetResponse, code=200)  #在底下的"Responses"可看到的文字內容
   @jwt_required()  #需要在postman上的"Authorization"登入token(login的時候拿到的)才能使用此功能
   def get(self, **kwargs):
       db, cursor = db_init()
       name = kwargs.get("name")   #取得剛剛input的"name"
       if name is not None:
           sql = f"SELECT * FROM test.user WHERE name = '{name}';"
       else:
           sql = 'SELECT * FROM test.user;'   #沒輸就整個table列出來
 
       cursor.execute(sql)
       users = cursor.fetchall()
       db.close()
       return util.success(users)  #秀出成功訊息(引用util.py)
 
   # Create User
   @doc(description="Create user data", tags=["User"])  
   @use_kwargs(user_swagger_model.UserPostSchema, location="form")  #新增可以填寫parameter(新user的data)並提交的功能
   @marshal_with(user_swagger_model.UserCommonResponse, code=201)
   def post(self, **kwargs):
       db, cursor = db_init()
       user = {
           'name': kwargs['name'],   #取得剛剛input的name
           'account': kwargs['account'],  #取得剛剛input的account
           'password': kwargs['password'],  #取得剛剛input的password
           'gender': kwargs['gender'],  #取得剛剛input的gender
           'birth': kwargs.get('birth') or '1900-01-01',  #取得剛剛input的birth
           'note': kwargs.get('note')  #取得剛剛input的note
       }
       sql = """
       INSERT INTO `test`.`member` (`name`,`gender`,`account`,`password`,`birth`,`note`)
       VALUES ('{}','{}','{}','{}','{}','{}');
       """.format(user['name'], user['gender'], user['account'], user['password'], user['birth'], user['note'])
       result = cursor.execute(sql)
       db.commit()
       db.close()
 
       if result == 0:   #沒填完整就報錯
           return util.failure({"message": "error"})
       return util.success()
 
 
class User(MethodResource):
   # Get data by id
   @doc(description="Get user data", tags=["User"])  
   @marshal_with(user_swagger_model.UserGetResponse, code=200)
   @jwt_required()
   def get(self, id):  #只要填入id就能查詢
       db, cursor = db_init()
       sql = f"SELECT * FROM test.user WHERE id = '{id}';"
       cursor.execute(sql)
       users = cursor.fetchall()
       db.close()
       return util.success(users)
   
   # Update data by id
   @doc(description="Update user data", tags=["User"])  
   @use_kwargs(user_swagger_model.UserPatchSchema, location="form")
   @marshal_with(user_swagger_model.UserCommonResponse, code=201)
   def patch(self, id, **kwargs):
       db, cursor = db_init()
       user = {
           'name': kwargs.get('name'),
           'account': kwargs.get('account'),
           'password': kwargs.get('password'),
           'gender': kwargs.get('gender'),
           'birth': kwargs.get('birth'),
           'note': kwargs.get('note')
        }
 
       query = []
       '''{'name': None, 'gender': 'Double', 'birth': None, 'note': None}'''
       for key, value in user.items():
           if value is not None:
               query.append(f"{key} = '{value}'")
       query = ",".join(query)

       sql = """
           UPDATE test.user
           SET {}
           WHERE id = {};
       """.format(query, id)
 
       result = cursor.execute(sql)
       db.commit()
       db.close()
 
       if result == 0:
           return util.failure({"message": "error"})
       return util.success()
   
   # Delete data by id
   @doc(description="Delete user data", tags=["User"])  
   @marshal_with(None, code=204)  
   def delete(self, id):
       db, cursor = db_init()
       sql = f'DELETE FROM `test`.`user` WHERE id = {id};'
       result = cursor.execute(sql)
       db.commit()
       db.close()
       return util.success()
 
class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(user_swagger_model.LoginSchema, location="form")
    #@marshal_with(user_swagger_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM test.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})
