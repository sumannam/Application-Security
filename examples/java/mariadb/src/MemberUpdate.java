import java.sql.*;
import java.util.Scanner;

public class MemberUpdate {
    public static void main(String[] args) {
        // 1. DB 연결 정보
        String url = "jdbc:mariadb://192.168.100.20:3306/cju";
        String dbUser = "cjulib";
        String dbPass = "security";

        Scanner sc = new Scanner(System.in);

        System.out.println("=== 회원 정보 수정 ===");
        System.out.print("수정할 회원의 번호(seq) 입력: ");
        int targetSeq = sc.nextInt();
        sc.nextLine(); // 숫자 입력 후 남은 엔터 제거

        System.out.print("새 비밀번호 입력: ");
        String newPass = sc.nextLine();

        System.out.print("새 이름 입력: ");
        String newName = sc.nextLine();

        // 2. 수정을 위한 SQL 문 (비밀번호와 이름 수정)
        String sql = "UPDATE member SET pass = ?, name = ? WHERE seq = ?";

        // 3. JDBC 실행
        try (Connection conn = DriverManager.getConnection(url, dbUser, dbPass);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            // '?' 순서대로 값 채우기
            pstmt.setString(1, newPass);
            pstmt.setString(2, newName);
            pstmt.setInt(3, targetSeq);

            // 4. 실행 및 결과 확인
            int result = pstmt.executeUpdate();

            if (result > 0) {
                System.out.println("[성공] " + targetSeq + "번 회원의 정보가 수정되었습니다.");
            } else {
                System.out.println("[실패] 해당 번호의 회원을 찾을 수 없습니다.");
            }

        } catch (SQLException e) {
            System.err.println("[오류] 수정 작업 중 문제가 발생했습니다: " + e.getMessage());
        }
    }
}