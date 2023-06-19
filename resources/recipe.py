from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection

# Resource : 데이터의 코드 만드는 Class

# API 동작하는 코드를 만들기 위해서는 class(클래스)를 만들어야 한다.

# class 란? 비슷한 데이터끼리 모아놓은 것 (Table을 생각) : class는 상속이 가능.
# class는 변수와 함수로 구성된 묶음
# Table과 다른 점; : 함수가 있다는 점

# API를 만들기 위한 class는
# flask_restful 라이브러리의 Resource class를 상속해서 생성.

class RecipeResource(Resource): # 경로가 다르면 새로운 클래스 Resource는 flask 꺼
    # GET 메소드에서 경로로 넘어오는 변수는 get 함수의 파라미터로 사용
    def get(self, recipe_id): # recipe_id를 입력한다
            # 위의 recipe_id 에 담겨있다.
        # 1. 클라이언트로부터 데이터를 받아온다.
        print(recipe_id)
        print(type(recipe_id))

        # 2. 데이터베이스에 레시피 아이디로 쿼리한다.(recipe/1~x)
        try :
            connection = get_connection()
            query = '''select r.*, u.username
                        from recipe r
                        join user u
                            on r.user_id= u.id
                        where r.id =%s;'''
            record= (recipe_id,) # 정수 하나면 ()라도 튜플이 아니고 그냥 정수니까 ","를 넣어준다.
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list= cursor.fetchall()
            print(result_list)
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {"result": "Fail", "error": str(e) }, 500
        
        # 3. 결과를 클라이언트에 응답한다.
        i = 0
        for row in result_list :
            result_list[i]['created_at']= row['created_at'].isoformat() # 문자열 변환
            result_list[i]['updated_at']= row['updated_at'].isoformat() # 문자열 변환
            i = i + 1

        # 없는 아이디를 넣으면 에러뜬다. 조건문으로 바꿔준다
        if len(result_list) != 1: # 항상 비정상일 경우를 상정해서 처리한다.
            return {"result": "success", "item": {} }
        else :
            return {"result": "success", "item": result_list[0]}

    @jwt_required() # 뭔..블락 리스트에 넣어..야.. 뭐라.. 암튼 필수  
    def put(self, recipe_id):
        # 1. 클라이언트로부터 데이터를 받아온다.
        print(recipe_id)
        print(type(recipe_id))
        
        # 1-1. header에 담긴 JWT 토큰을 받아온다.(user_id 받아온다)
        user_id= get_jwt_identity()

        # body에 있는 json 데이터를 받아온다.
        data= request.get_json()
        print(data)
        
        # 2. 데이터베이스에 update 한다.
        try :
            connection = get_connection()
            query= """update recipe
                        set name = %s, description=%s,
                        num_of_servings= %s, cook_time= %s,
                        directions= %s, is_publish= %s
                        where id = %s and user_id=%s;"""
            # 위에서 쓸 데이터는 pastman body 안에 넣는다 json으로
            record= ( data['name'], data['description'],
                    data['num_of_servings'], data['cook_time'],
                    data['directions'], data['is_publish'],
                    recipe_id, user_id)
            cursor= connection.cursor()
            cursor.execute(query, record)
            
            connection.commit()
            
            cursor.close()
            connection.close()
        
        except Error as e :
            print(e)
            return{"result":"success", "error": str(e)},500
        return {"result":"success"}
    @jwt_required()
    def delete(self, recipe_id):
        # 1. 클라이언트로부터 데이터를 받아온다.
        print(recipe_id)
        # 1-1. header에 담긴 JWT 토큰을 받아온다.(user_id 받아온다)
        user_id= get_jwt_identity()
        # 2. DB에서 삭제한다.
        try:
            connection= get_connection()
            query = """delete from recipe where id = %s and user_id= %s;"""
            record= (recipe_id, user_id)
            cursor= connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {"result":"success", "error":str(e)}
        # 3. 결과를 응답한다.
        
        return {"result":"succes"}

class RecipeListResource(Resource): # class 클래스 이름(상속 받을 변수,함수):
    @jwt_required()
    def post(self) : # class 안의 def 함수 입력 값은 self
        # PostMan(클라이언트)에서 POST 요청을 받아서 해당 POST 함수를 실행
        # {
        #     "name": "김치찌게",
        #     "description": "맛있게 끓이는 방법",
        #     "num_of_servings": 4,
        #     "cook_time": 30,
        #     "directions": "고기볶고 김치넣고 물뭇고 두부넣고",
        #     "is_publish": 1
        # }
        
        # 1. 클라이언트가 보낸 데이터를 받아온다. (유저의 요청을 받음)
        data = request.get_json()
        
        # 1-1. header에 담긴 JWT 토큰을 받아온다.
        user_id= get_jwt_identity()
        
        print(data)
        
        # 2. DB에 저장한다.
        try :
            # 2-1. 데이터베이스를 연결한다. 
            connection = get_connection()

            # 2-2. 쿼리문을 만든다.
# # # # 칼럼과 매칭되는 데이터만 %s(포맷팅: 유저입력)로 바꿔준다. # # # # 
            query = '''insert into recipe
                    (name, description, num_of_servings,
                    cook_time, directions, is_publish, user_id)
                    values
                    (%s, %s, %s, %s, %s, %s, %s);'''
            # 2-3. 쿼리에 매칭되는 변수 처리 ★중요★ 튜플로 처리한다.
            record = ( data['name'], data['description'],
                        data['num_of_servings'], data['cook_time'],
                        data['directions'], data['is_publish'],
                        user_id)
            # 2-4. 커서를 가져온다.
            cursor = connection.cursor()
            # 2-5. 쿼리문을 실행한다.
            cursor.execute(query, record)
            # 2-6. DB에 반영 완료하라는 commit 해줘야 한다.
            connection.commit()
            # 2-7. 자원해제
            cursor.close()
            connection.close()
            

        except Error as e :  # Erorr는 mysql 라이브러리
            print(e)
            return {'result' : 'fail', 'error' : str(e) }, 500
        
        # 3. 에러가 났으면, 에러 라고 알려주고, 아니면 잘 저장되었다고 알려준다.

        # 응답할 땐(return) JSON으로 작성 
        return {"result" : "success"}
    
    def get(self) :
        # 1. 클라이언트로 부터 데이터를 받아온다.
        
        # 2. 저장된 레시피 리스트를 DB로부터 가져온다.
        
        # 2-1. DB 커넥션
        
        try:
            connection = get_connection()
        
        # 2-2. 쿼리문 만든다.
            query='''select r.*, u.username
                    from recipe r
                    join user u
                        on r.user_id= u.id
                    where is_publish =1;'''
        
        # 2-3. 변수 처리할 부분은 변수 처리 한다.
        # 없음
        
        # 2-4. 커서 가져온다.
            cursor = connection.cursor(dictionary= True) # dic파라미터:True:json 반환
    
        # 2-5 쿼리문을 커서로 실행한다.
            cursor.execute(query)
        
        # 2-6. 실행 결과를 가져온다.
            result_list= cursor.fetchall()
            print(result_list)

            cursor.close()
            connection.close()
        except Error as e :
            print(e)
            return {'result': 'fail', 'error': str(e) } , 500
            
        # 3. 데이터가공이 필요하면 가공 후 클라이언트에 응답한다.
        i = 0
        for row in result_list :
            result_list[i]['created_at']= row['created_at'].isoformat() # 문자열 변환
            result_list[i]['updated_at']= row['updated_at'].isoformat() # 문자열 변환
            i = i + 1
            
        return {'result' : 'success',
                'count' : 3,
                'items' : result_list} # 200=정상=작성NO, 그외는 상태코드 리턴




class UserRecipeResource(Resource): # 여기 막힘

    def get(self, user_id):
        # 2. 데이터베이스에 레시피 아이디로 쿼리한다.(recipe/1~x)
        try :
            connection = get_connection()
            query = '''select r.*, u.username
                        from recipe r
                        join user u
                            on r.user_id= u.id
                        where recipe_id = %s and u.id=%s;'''
            record= (user_id,) # 정수 하나면 ()라도 튜플이 아니고 그냥 정수니까 ","를 넣어준다.
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list= cursor.fetchall()
            print(result_list)
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {"result": "Fail", "error": str(e) }, 500






