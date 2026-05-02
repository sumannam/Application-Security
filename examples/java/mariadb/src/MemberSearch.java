import java.sql.*;
import java.util.Scanner;

public class MemberSearch {
    public static void main(String[] args) {
        // 1. DB 연결 정보 (사용자 환경에 맞게 수정)
        String url = "jdbc:mariadb://192.168.100.20:3306/cju";
        String dbUser = "cjulib";
        String dbPass = "security";

        Scanner sc = new Scanner(System.in);
        System.out.print("검색할 회원 seq를 입력하세요: ");
        String searchId = sc.nextLine();

        // 2. SQL 쿼리 (특정 ID의 정보를 가져옴)
        String sql = "SELECT seq, id, pass, name FROM member WHERE seq = ?";

        // 3. 실행 (try-with-resources로 리소스 자동 반납)
        try (Connection conn = DriverManager.getConnection(url, dbUser, dbPass);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            // '?' 자리에 검색할 ID를 안전하게 세팅 (SQL Injection 방어!)
            pstmt.setString(1, searchId);

            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    // 데이터가 있을 경우 출력
                    int seq = rs.getInt("seq");
                    String id = rs.getString("id");
                    String pass = rs.getString("pass");
                    String name = rs.getString("name");

                    System.out.println("\n[ 회원 정보 검색 결과 ]");
                    System.out.println("------------------------------------");
                    System.out.println("일련번호(Seq): " + seq);
                    System.out.println("아이디(ID): " + id);
                    System.out.println("비밀번호(Pass): " + pass);
                    System.out.println("이름(Name): " + (name == null ? "미등록" : name));
                    System.out.println("------------------------------------");
                } else {
                    System.out.println("[알림] 해당 ID를 가진 회원이 존재하지 않습니다.");
                }
            }

        } catch (SQLException e) {
            System.err.println("[오류] DB 작업 중 예외 발생: " + e.getMessage());
        }
    }
}