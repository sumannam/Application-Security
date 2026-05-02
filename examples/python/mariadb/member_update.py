import pymysql

# 1. DB 접속 정보 설정
db_config = {
    'host': '192.168.100.20',
    'user': 'cjulib',
    'password': 'security',
    'db': 'cju',
    'charset': 'utf8mb4'
}

def update_member_name():
    print("========= 회원 이름 수정 예제 (UPDATE) =========")
    
    try:
        # 수정할 대상 번호와 새 이름 입력 받기
        target_seq = input("수정할 회원의 번호(seq) 입력: ")
        new_name = input("변경할 새 이름 입력: ")

        # 2. DB 연결
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 3. SQL 실행 (특정 seq의 name만 변경)
        # [주의] WHERE 절이 없으면 모든 행의 이름이 변경됩니다!
        sql = "UPDATE member SET name = %s WHERE seq = %s"
        
        # execute()의 두 번째 인자로 튜플 형태로 값을 전달 (SQL 인젝션 방지)
        result_count = cursor.execute(sql, (new_name, target_seq))

        if result_count == 0:
            print(f"\n[알림] 번호 {target_seq}번에 해당하는 회원이 없습니다.")
        else:
            # 4. 변경사항 확정
            conn.commit()
            print(f"\n[성공] {target_seq}번 회원의 이름이 '{new_name}'(으)로 수정되었습니다.")

    except pymysql.MySQLError as e:
        print(f"\n[오류] 데이터 수정 실패: {e}")
        if conn: conn.rollback()

    finally:
        # 5. 자원 해제
        if conn: conn.close()

if __name__ == "__main__":
    update_member_name()