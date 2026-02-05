import java.sql.*;
import java.util.*;
import java.util.List;

public class LibraryRepository {
    // DB 연결 정보
    private final String URL = "jdbc:mariadb://192.168.100.20:3306/library";
    private final String USER = "cjulib";
    private final String PASSWORD = "security";

    /**
     * MariaDB 연결을 위한 전용 메소드입니다.
     * <p>JDBC 드라이버를 로드하고 설정된 정보를 바탕으로 {@link Connection} 객체를 생성합니다.</p>
     * * @return 데이터베이스 연결 객체
     * @throws SQLException 드라이버 로드 실패 또는 연결 정보가 부적절할 경우 발생
     *
     * @see <a href="https://mariadb.com/kb/en/about-mariadb-connector-j/">MariaDB Connector/J Documentation</a>
     */
    private Connection getConnection() throws SQLException {
        try {
            Class.forName("org.mariadb.jdbc.Driver"); //
        } catch (ClassNotFoundException e) {
            throw new SQLException("드라이버 로드 실패: " + e.getMessage());
        }
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }

    /**
     * 메모리의 모든 도서 정보를 MariaDB에 동기화(저장)합니다.
     * <p>기존 CSV의 '전체 저장' 기능을 DB의 Upsert(Insert or Update) 로직으로 변환하여 구현하였습니다.</p>
     * <p>성능 최적화를 위해 Batch 처리를 수행하며, 중복된 ID가 있을 경우 정보를 업데이트합니다.</p>
     * * @param bookMap 동기화할 도서 데이터 맵
     *
     * @see <a href="https://github.com/sumannam/Java/issues/22">Issue #22: 종료 시 데이터 영속화 문제 해결</a>
     */
    public void saveBooks(Map<Integer, Book> bookMap) {
        // 중복된 ID가 있으면 업데이트, 없으면 삽입하는 MariaDB 쿼리
        String sql = "INSERT INTO books (book_id, title, author, is_available, member_id) " +
                "VALUES (?, ?, ?, ?, ?) " +
                "ON DUPLICATE KEY UPDATE " +
                "title = VALUES(title), " +
                "author = VALUES(author), " +
                "is_available = VALUES(is_available), " +
                "member_id = VALUES(member_id)";

        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            // 성능 최적화를 위한 배치(Batch) 처리
            for (Book book : bookMap.values()) {
                pstmt.setInt(1, book.getId());
                pstmt.setString(2, book.getTitle());
                pstmt.setString(3, book.getAuthor());
                pstmt.setBoolean(4, book.isAvailable());

                // 대출자가 "null" 문자열인 경우 DB 실제 NULL로 처리
                if (book.getBorrowerId() == null || "null".equals(book.getBorrowerId())) {
                    pstmt.setNull(5, java.sql.Types.VARCHAR);
                } else {
                    pstmt.setString(5, book.getBorrowerId());
                }
                pstmt.addBatch(); // 대기열에 추가
            }

            pstmt.executeBatch(); // 한 번에 실행
            System.out.println("[시스템] 모든 도서 데이터가 MariaDB에 동기화되었습니다.");

        } catch (SQLException e) {
            System.err.println("[오류] DB 저장(saveBooks) 실패: " + e.getMessage());
        }
    }

    /**
     * 데이터베이스로부터 모든 도서 정보를 조회하여 메모리에 로드합니다.
     * * @return 도서 ID를 키로 하는 도서 정보 맵
     * @see <a href="https://github.com/sumannam/Java/issues/23">Issue #23: 초기 구동 시 DB 데이터 로딩</a>
     */
    public Map<Integer, Book> loadBooks() {
        Map<Integer, Book> bookMap = new HashMap<>();
        String sql = "SELECT * FROM books";

        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            while (rs.next()) {
                int id = rs.getInt("book_id");
                String title = rs.getString("title");
                String author = rs.getString("author");
                boolean available = rs.getBoolean("is_available");
                String mid = rs.getString("member_id");

                bookMap.put(id, new Book(id, title, author, available, mid == null ? "null" : mid));
            }
        } catch (SQLException e) {
            System.err.println("[오류] 로드 실패: " + e.getMessage());
        }
        return bookMap;
    }

    /**
     * 사용자 로그인을 위한 정보를 조회합니다.
     * <p><b>보안 실습 주의:</b> 현재 이 메소드는 SQL Injection 공격에 취약하도록 의도적으로 설계되었습니다.</p>
     * <p>입력값이 쿼리문에 직접 결합되는 방식의 위험성을 교육하기 위한 용도로만 사용하십시오.</p>
     * * @param id 사용자 아이디
     * @param pw 사용자 비밀번호
     * @return 인증된 {@link User} 객체 (일치 정보 없을 시 null)
     *
     * @see <a href="https://github.com/sumannam/Java/issues/40">Issue #40: SQL Injection 취약점 개발</a>
     */
    public User loadUser(String id, String pw) {
        //String sql = "SELECT * FROM users WHERE user_id = ? AND password = ?";
        String sql = "SELECT * FROM users WHERE user_id = '" + id + "' AND password = '" + pw + "'";
        //System.out.println(sql);

        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, id);
            pstmt.setString(2, pw);

            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    // 반환 타입이 User로 바뀌었으므로 이제 에러 없이 정상 작동합니다.
                    return new User(
                            rs.getString("user_id"),
                            rs.getString("password"),
                            rs.getString("type")
                    );
                }
            }
        } catch (SQLException e) {
            System.err.println("[오류] 로그인 조회 실패: " + e.getMessage());
        }
        return null; // 일치하는 사용자가 없을 때
    }
}