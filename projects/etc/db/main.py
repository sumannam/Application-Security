from insecure.MariaDBClient import MariaDBClient

def main():
    # MariaDB 연결 정보
    host = input("Host: ").strip() or "192.168.100.20"
    user = input("User: ").strip() or "root"
    password = input("Password: ").strip() or "security"
    database = input("Database: ").strip() or "cju"

    # 클라이언트 생성 및 연결
    client = MariaDBClient(host, user, password, database)
    if not client.connect():
        return

    try:
        while True:
            # SQL 쿼리 입력 받기
            query = input("\nSQL> ").strip()
            
            if query.lower() in ('exit', 'quit'):
                break
                
            if not query:
                continue

            # 쿼리 실행
            result = client.execute_query(query)
            
            # 결과 출력
            if result is not None:
                if isinstance(result, list):
                    for row in result:
                        print(row)
                else:
                    print(f"Affected rows: {result}")

    finally:
        client.disconnect()

if __name__ == "__main__":
    main()