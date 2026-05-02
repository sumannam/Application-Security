import pymysql

# 1. DB 접속 정보 설정
db_config = {
    'host': '192.168.100.20',
    'user': 'cjulib',
    'password': 'security',
    'db': 'cju',
    'charset': 'utf8mb4'
}

def delete_member_data():
    print("========= 회원 정보 삭제 예제 (DELETE) =========")
    
    try:
        # 삭제할 대상 번호 입력 받기
        target_seq = input("삭제할 회원의 번호(seq) 입력: ")

        # 2. DB 연결
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 3. SQL 실행 (특정 seq를 가진 행 삭제)
        # [주의] WHERE 절이 없으면 테이블의 모든 데이터가 삭제됩니다!
        sql = "DELETE FROM member WHERE seq = %s"
        
        # SQL 인젝션 방지를 위해 파라미터 바인딩 사용
        result_count = cursor.execute(sql, (target_seq,))

        if result_count == 0:
            print(f"\n[알림] 번호 {target_seq}번에 해당하는 회원이 존재하지 않습니다.")
        else:
            # 4. 변경사항 확정 (DELETE 역시 commit이 필수입니다)
            conn.commit()
            print(f"\n[성공] {target_seq}번 회원의 정보가 삭제되었습니다.")

    except pymysql.MySQLError as e:
        print(f"\n[오류] 데이터 삭제 실패: {e}")
        if conn: conn.rollback() # 에러 발생 시 삭제 취소

    finally:
        # 5. 자원 해제
        if conn: conn.close()

if __name__ == "__main__":
    delete_member_data()