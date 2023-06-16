from flask import Flask # from f:소문자, import F:대문자
from flask_restful import Api # A 구분
from resources.recipe import RecipeListResource, RecipeResource

app= Flask(__name__) # 여기도 F:대문자

api = Api(app) # api 변수에 Flask를 넣음

# 경로(URL의 path:포트뒤/path/쿼리앞)와 API동작코드(Resource)를 연결한다.
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>') # recipes/숫자 들어오면 쉼표 앞을 실행

# 클라이언트(PostMan)에게 요청 받고 
# 요청 받은 URL이 '/recipes'가 맞다면 /recipes 경로로 넘어와서 앞에 RecipeListResource 실행
# 폴더명: resource,  파일명: recipe.py


if __name__== '__main__':
    app.run()
# 위 코드를 Ctrl+F5 = python app.py, URL로 요청이 들어오면 처리한다.

