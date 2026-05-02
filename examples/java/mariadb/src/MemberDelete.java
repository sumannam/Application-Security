import java.sql.*;
import java.util.Scanner;

public class MemberDelete {
    public static void main(String[] args) {
        // 1. DB 연결 정보
        String url = "jdbc:mariadb://192.168.100.20:3306/cju";
        String dbUser = "cjulib";
        String dbPass = "security";

        Scanner sc = new Scanner(System.in);
        System.out.print("삭제할 회원의 번호(seq)를 입력하세요: ");
        int targetSeq = sc.nextInt();

        // 2. 삭제를 위한 SQL 문
        String sql = "DELETE FROM member WHERE seq = ?";

        // 3. JDBC 실행
        try (Connection conn = DriverManager.getConnection(url, dbUser, dbPass);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            // '?' 자리에 삭제할 번호 세팅
            pstmt.setInt(1, targetSeq);

            // 4. executeUpdate() 실행
            // 삭제, 수정, 삽입은 executeQuery() 대신 executeUpdate()를 사용합니다.
            int result = pstmt.executeUpdate();

            // 5. 결과 확인
            if (result > 0) {
                System.out.println("[성공] " + targetSeq + "번 회원 데이터가 삭제되었습니다.");
            } else {
                System.out.println("[실패] 해당 번호의 회원이 존재하지 않습니다.");
            }

        } catch (SQLException e) {
            System.err.println("[오류] 삭제 작업 중 문제가 발생했습니다: " + e.getMessage());
        }
    }
}