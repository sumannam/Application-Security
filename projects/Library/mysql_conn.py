import mariadb
import sys

# 접속 정보 설정
config = {
    "host": "192.168.100.20",
    "port": 3306,
    "user": "cjulib",
    "password": "security",
    "database": "library"
}

try:
    # 1. 데이터베이스 연결
    conn = mariadb.connect(**config)
    print(f"Successfully connected to MariaDB at {config['host']}")

    # 2. 커서(Cursor) 생성
    cur = conn.cursor()

    # 3. member 테이블 조회 쿼리 실행
    print("\n--- [member 테이블 조회 결과] ---")
    cur.execute("SELECT * FROM members")

    # 컬럼(열) 이름 출력 (선택 사항)
    column_names = [i[0] for i in cur.description]
    print(f"컬럼명: {column_names}")
    print("-" * 30)

    # 데이터 가져오기 및 출력
    rows = cur.fetchall() # 모든 데이터 가져오기

    if not rows:
        print("조회된 데이터가 없습니다.")
    else:
        for row in rows:
            print(row)

except mariadb.Error as e:
    print(f"MariaDB 연결 또는 쿼리 오류: {e}")
    sys.exit(1)

finally:
    # 4. 연결 종료
    if 'conn' in locals():
        conn.close()
        print("\n연결이 안전하게 종료되었습니다.")