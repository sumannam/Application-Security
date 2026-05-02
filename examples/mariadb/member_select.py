import pymysql

# 1. DB 접속 정보 설정
db_config = {
    'host': '192.168.100.20',
    'user': 'cjulib',
    'password': 'security',
    'db': 'cju',
    'charset': 'utf8mb4'
}

def select_member_data():
    print("===========================================================")
    print(" [회원 목록 조회 결과]")
    print(f" {'번호':<4} | {'아이디':<12} | {'비밀번호':<15} | {'이름':<10}")
    print("-----------------------------------------------------------")

    conn = None
    try:
        # 2. DB 연결
        conn = pymysql.connect(**db_config)
        # 딕셔너리 형태로 결과를 받으면 컬럼명으로 접근하기 쉬워 학생들에게 추천하기 좋습니다.
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 3. SELECT 쿼리 실행
        sql = "SELECT seq, id, `pass`, name FROM member ORDER BY seq DESC"
        cursor.execute(sql)

        # 4. 모든 결과 가져오기
        rows = cursor.fetchall()

        if not rows:
            print("  등록된 회원 정보가 없습니다.")
        else:
            for row in rows:
                # DB 컬럼 값을 변수에 매핑
                seq = row['seq']
                user_id = row['id']
                user_pw = row['pass']
                user_name = row['name'] if row['name'] else "N/A"

                print(f" {seq:<5} | {user_id:<13} | {user_pw[:15]:<15}... | {user_name:<11}")

    except pymysql.MySQLError as e:
        print(f"\n[오류] 데이터 조회 실패: {e}")

    finally:
        # 5. 자원 해제
        if conn:
            conn.close()
    print("===========================================================")

if __name__ == "__main__":
    select_member_data()