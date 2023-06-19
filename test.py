from mysql_connection import get_connection
from mysql.connector import Error

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