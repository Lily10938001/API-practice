!pip install flask-apispec
!pip install flask-jwt-extended

import flask
from flask_restful import Api
from resource.user2 import Users, User, Login

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin  #製作網頁的東東
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager  #設定login元件的東東

# Flask設定
app = flask.Flask(__name__)

# Flask restful設定
api = Api(app)

app.config["DEBUG"] = True  #存檔時直接rerun一次,就不用再ctrl+c
app.config["JWT_SECRET_KEY"] = "secret_key" #JWT token設定 

app.config.update({    #建立swagger網頁
   'APISPEC_SPEC': APISpec(
       title='Awesome Project',
       version='v1',
       plugins=[MarshmallowPlugin()],
       openapi_version='2.0.0'
   ),
   'APISPEC_SWAGGER_URL': '/swagger/',  # URL格式
   'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # UI介面的URL格式
})
docs = FlaskApiSpec(app)

# 定義URL(router)
api.add_resource(Users, "/users")  #顯示Class為Users的提示文字
docs.register(Users)

api.add_resource(User, "/user/<int:id>")   #顯示Class為User的提示文字
docs.register(User)

api.add_resource(Login, "/login")   #顯示Class為login的提示文字
docs.register(Login)

# py3預設的名字為main,此行是確保事py3是由name執行
if __name__ == '__main__':
    # flask server預定的localhost ip ,80誒是域定的port號
    jwt = JWTManager().init_app(app)
    app.run(host='127.0.0.1', port=10000)
