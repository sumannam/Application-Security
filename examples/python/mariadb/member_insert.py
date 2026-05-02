# pip install pymysql

import pymysql

# 1. 데이터베이스 접속 정보 설정
db_config = {
    'host': '192.168.100.20',
    'user': 'cjulib',
    'password': 'security',
    'db': 'cju',
    'charset': 'utf8mb4'
}

def insert_member_data():
    print("========= 회원 정보 등록 예제 (Table: member) =========")
    
    # 사용자로부터 데이터 입력 받기
    user_id = input("아이디(id) 입력 : ")
    user_pw = input("비밀번호(pass) 입력 : ")
    user_name = input("이름(name) 입력 : ")

    conn = None
    try:
        # 2. DB 연결 및 커서 생성
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 3. SQL 실행 (seq는 자동 증가이므로 제외)
        # 컬럼명 'pass'는 SQL 예약어와 겹칠 수 있으므로 백틱(`)으로 감싸는 것이 안전합니다.
        sql = "INSERT INTO member (id, `pass`, name) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, user_pw, user_name))

        # 4. 트랜잭션 확정 (반드시 호출해야 DB에 반영됨)
        conn.commit()
        print("\n[성공] 새로운 회원 정보가 성공적으로 추가되었습니다.")

    except pymysql.MySQLError as e:
        print(f"\n[오류] 데이터베이스 작업 실패: {e}")
        if conn:
            conn.rollback()  # 오류 발생 시 작업 취소

    finally:
        # 5. 연결 종료
        if conn:
            conn.close()

if __name__ == "__main__":
    insert_member_data()