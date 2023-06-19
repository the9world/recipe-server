```python
connection= get_connection()
query= '''select * from user
            where email = %s;'''
record= (data['email'],)

cursor= connection.cursor(dictionary=True)
cursor.execute(query, record)

result_list= cursor.fetchall()
```
- Python에서 MySQL 데이터베이스에 연결하고  
쿼리를 실행하여 결과를 가져오는 예시입니다.

- connection = get_connection(): get_connection() 함수를 호출하여  
MySQL 데이터베이스에 연결하는 커넥션 객체인 connection을 생성.  
이 함수는 데이터베이스 연결을 설정하고 연결된 커넥션 객체를 반환.

- query = '''select * from user where email = %s;''': query 변수에 SQL 쿼리를 할당.  
이 예시에서는 user 테이블에서 이메일이 주어진 값과 일치하는 모든 레코드를 선택하는 쿼리.  
%s는 나중에 플레이스홀더에 대체될 값을 나타냅니다.

- record = (data['email'],): record 변수에 튜플 형태로 데이터를 할당.  
이 예시에서는 data 딕셔너리의 'email' 키에 해당하는 값을 사용.  
플레이스홀더에 대체될 값이 튜플 형태로 제공되어야 함.  
여기서 튜플의 콤마(,)는 단일 요소의 튜플을 생성하기 위해 필요합니다.  

- cursor = connection.cursor(dictionary=True): connection 객체의 cursor 메서드를 호출하여 커서 객체 cursor를 생성.  
dictionary=True 인자는 딕셔너리 형식의 결과를 반환하도록 커서를 설정하는 것을 의미.  
이렇게 하면 결과를 열 이름을 키로 갖는 딕셔너리 형태로 가져올 수 있습니다.  

- cursor.execute(query, record): cursor 객체의 execute 메서드를 호출하여 쿼리를 실행  
query 변수에 저장된 쿼리를 실행하고, record 변수에 저장된 데이터를 플레이스홀더에 대체하여 실행합니다.  

- result_list = cursor.fetchall(): cursor 객체의 fetchall 메서드를 호출하여 모든 결과를 가져옴.  
fetchall은 실행된 쿼리의 결과를 모두 가져와 리스트 형태로 반환합니다.  

- 위의 코드를 실행하면 데이터베이스에서 해당 이메일을 가진 사용자를 선택한 결과를 result_list 변수에 저장하게 됩니다.  
이후에는 result_list를 활용하여 필요한 작업을 수행할 수 있음.  
마지막으로 커서와 커넥션을 닫아 데이터베이스 연결을 정리해야 합니다.

---
```python
@jwt_required()
def delete(self):
    jti= get_jwt()['jti']
    print(jti)
    jwt_blocklist.add(jti)
```
- Flask와 Flask-JWT-Extended를 사용하여  
JWT (JSON Web Token) 인증이 필요한 엔드포인트에서 특정 JWT를  
블록 리스트에 추가하는 예시

- @jwt_required(): @jwt_required() 데코레이터는 해당 엔드포인트에 JWT 인증이 필요하다는 것을 나타냄.  
이를 통해 엔드포인트에 접근하기 위해서는 요청 헤더에 유효한 JWT가 포함되어야 함.  
만약 JWT가 유효하지 않거나 제공되지 않은 경우, 인증 오류가 발생함.

- def delete(self): delete 메서드는 해당 엔드포인트에서 수행되는 작업을 정의하는  
메서드. 이 예시에서는 JWT 블록 리스트에 특정 JWT를 추가하는 작업을 수행.

- jti = get_jwt()['jti']: get_jwt() 함수를 호출하여  
현재 요청에 대한 JWT 정보를 가져옴. JWT에는 여러 정보가 포함될 수 있으며,  
여기서는 JWT의 'jti' (JWT ID)를 가져옴. 'jti'는 각 JWT의 고유 식별자로 사용됨.

- print(jti): 'jti' 값을 출력함. 단순히 디버깅이나 테스트를 위한 용도.

- jwt_blocklist.add(jti): jwt_blocklist라는 이름의 객체(예: 세트(Set))에  
'jti' 값을 추가함. 이를 통해 JWT 블록 리스트에 해당 JWT를 추가하여  
나중에 유효성 검사에서 블록된 JWT로 처리할 수 있음.  
jwt_blocklist 객체는 유효하지 않은 JWT의 블록 목록을 관리하려 사용되는 것으로 가정.

- 위의 코드는 JWT 인증이 필요한 엔드포인트에서  
현재 요청에 대한 JWT의 'jti' 값을 가져와서 출력한 후,  
해당 'jti' 값을 JWT 블록 리스트에 추가함.  
이를 통해 블록된 JWT는 나중에 인증 요청 시 거부될 수 있음.  
인증된 사용자의 로그아웃 또는 토큰의 무효화와 같은 시나리오에서 유용할 수 있음.