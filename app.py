from flask import Flask # from f:소문자, import F:대문자
from flask_restful import Api # A 구분
from config import Config 
from resources.recipe import RecipeListResource, RecipeResource, UserRecipeResource
from resources.user import UserLoginResource, UserLogoutResource
from resources.user import UserRegisterResource, jwt_blocklist
from flask_jwt_extended import JWTManager

app= Flask(__name__) # 여기도 F:대문자

# 환경변수 세팅
app.config.from_object(Config)

        # JWT 매니저 초기화
# Flask-JWT-Extended 확장에 대한
# JWT 설정 및 콜백 기능을 보유하는 데 사용되는 개체..?
jwt= JWTManager(app)

# 로그아웃된 토큰으로 요청하는 경우!  이 경우는 비정상적인 경우 이므로
# jwt가 알아서 처리하도록 코드작성 (함수는 정해져있다)
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app) # api 변수에 Flask를 넣음

# 경로(URL의 path:포트뒤/path/쿼리앞)와 API동작코드(Resource)를 연결한다.
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>') # recipes/숫자 들어오면 쉼표 앞을 실행
api.add_resource(UserRegisterResource, '/user/register') # 회원가입
api.add_resource(UserLoginResource, '/user/login') # 로그인
api.add_resource(UserLogoutResource, '/user/logout') # 로그아웃
api.add_resource(UserRecipeResource, '/user/recipes')


# 클라이언트(PostMan)에게 요청 받고 
# 요청 받은 URL이 '/recipes'가 맞다면 /recipes 경로로 넘어와서 앞에 RecipeListResource 실행
# 폴더명: resource,  파일명: recipe.py


if __name__== '__main__':
    app.run()
# 위 코드를 Ctrl+F5 = python app.py, URL로 요청이 들어오면 처리한다.


# 입력 id 암호화 $pip install flask-jwt-extended