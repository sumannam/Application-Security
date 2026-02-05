import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBconn {
    // 연결 정보 설정
    private static final String URL = "jdbc:mariadb://192.168.100.20:3306/library";
    private static final String USER = "cjulib";
    private static final String PASSWORD = "security";

    /**
     * 데이터베이스 연결 객체를 반환합니다.
     * @return Connection 객체
     */
    public static Connection getConnection() {
        Connection conn = null;
        try {
            // 1. 드라이버 로드 (생략 가능하나 명시적 로드 권장)
            Class.forName("org.mariadb.jdbc.Driver");

            // 2. 연결 수행
            conn = DriverManager.getConnection(URL, USER, PASSWORD);
            System.out.println("[시스템] MariaDB 연결 성공!");

        } catch (ClassNotFoundException e) {
            System.err.println("[오류] 드라이버를 찾을 수 없습니다: " + e.getMessage());
        } catch (SQLException e) {
            System.err.println("[오류] DB 연결 실패: " + e.getMessage());
        }
        return conn;
    }

    // 간단한 연결 테스트용 main
    public static void main(String[] args) {
        Connection testConn = getConnection();
        if (testConn != null) {
            try {
                testConn.close(); // 테스트 후 닫기
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}