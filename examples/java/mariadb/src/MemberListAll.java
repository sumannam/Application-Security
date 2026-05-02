import java.sql.*;

public class MemberListAll {
    public static void main(String[] args) {
        // 1. DB 연결 정보
        String url = "jdbc:mariadb://192.168.100.20:3306/cju";
        String dbUser = "cjulib";
        String dbPass = "security";

        // 2. 전체 조회를 위한 SQL 문
        String sql = "SELECT seq, id, pass, name FROM member ORDER BY seq ASC";

        System.out.println("======================================================");
        System.out.printf("| %-5s | %-10s | %-15s | %-10s |\n", "SEQ", "ID", "PASSWORD", "NAME");
        System.out.println("------------------------------------------------------");

        // 3. JDBC 실행
        try (Connection conn = DriverManager.getConnection(url, dbUser, dbPass);
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            int count = 0;
            // 4. ResultSet의 모든 레코드를 순회 (데이터가 없을 때까지 반복)
            while (rs.next()) {
                int seq = rs.getInt("seq");
                String id = rs.getString("id");
                String pass = rs.getString("pass");
                String name = rs.getString("name");

                // 표 형식으로 출력
                System.out.printf("| %-5d | %-10s | %-15s | %-10s |\n",
                        seq, id, pass, (name == null ? "-" : name));
                count++;
            }

            if (count == 0) {
                System.out.println("  등록된 회원이 없습니다.");
            }
            System.out.println("======================================================");
            System.out.println("[시스템] 총 " + count + "명의 회원을 조회했습니다.");

        } catch (SQLException e) {
            System.err.println("[오류] 전체 목록 조회 중 실패: " + e.getMessage());
        }
    }
}