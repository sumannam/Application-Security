import org.junit.jupiter.api.*;
import java.sql.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class LibraryRepositoryTest {

    private LibraryRepository repository;

    @BeforeEach
    void setUp() {
        repository = new LibraryRepository();

        // 테스트 시작 전 테이블 데이터를 초기화하여 독립적인 테스트 환경 구축
        clearTables();
    }

    /**
     * 테스트용 데이터가 꼬이지 않도록 모든 데이터를 삭제합니다.
     */
    private void clearTables() {
        // 외래 키 제약 조건 때문에 books 테이블을 먼저 삭제해야 합니다.
        String deleteBooks = "DELETE FROM books";
        String deleteUsers = "DELETE FROM users";

        // Repository 내부의 연결 설정을 활용하거나 직접 연결하여 초기화 수행
        // 여기서는 테스트 편의를 위해 직접 연결 예시를 포함합니다.
        try (Connection conn = DriverManager.getConnection(
                "jdbc:mariadb://192.168.100.20:3306/library", "cjulib", "security");
             Statement stmt = conn.createStatement()) {

            stmt.executeUpdate(deleteBooks);
            stmt.executeUpdate(deleteUsers);

            // 테스트를 위한 기본 사용자(admin) 추가
            stmt.executeUpdate("INSERT INTO users (user_id, password, type) VALUES ('admin', '1111', 'ADMIN')");

        } catch (SQLException e) {
            System.err.println("테스트 환경 초기화 실패: " + e.getMessage());
        }
    }

    @Test
    @DisplayName("DB 도서 데이터 저장 및 동기화 테스트 (saveBooks)")
    void saveBooks() {
        // Given: 저장할 도서 데이터 준비
        Map<Integer, Book> bookMap = new HashMap<>();
        bookMap.put(1, new Book(1, "DB 테스트 도서", "저자A", true, "null"));

        // When: DB 저장 실행 (UPSERT 로직 작동)
        repository.saveBooks(bookMap);

        // Then: DB에서 다시 불러와 데이터가 정확히 저장되었는지 확인
        Map<Integer, Book> loadedMap = repository.loadBooks();
        assertTrue(loadedMap.containsKey(1), "ID 1번 도서가 DB에 존재해야 합니다.");

        Book savedBook = loadedMap.get(1);
        assertEquals("DB 테스트 도서", savedBook.getTitle());
        assertEquals("저자A", savedBook.getAuthor());
    }

    @Test
    @DisplayName("DB로부터 도서 데이터 로드 테스트 (loadBooks)")
    void loadBooks() {
        // Given: 테스트 데이터를 먼저 DB에 저장
        Map<Integer, Book> originalMap = new HashMap<>();
        originalMap.put(100, new Book(100, "SQL 입문", "저자B", false, "admin"));
        repository.saveBooks(originalMap);

        // When: 로드 실행
        Map<Integer, Book> loadedMap = repository.loadBooks();

        // Then: 로드된 데이터 검증
        assertNotNull(loadedMap);
        assertTrue(loadedMap.size() >= 1);

        Book loadedBook = loadedMap.get(100);
        assertEquals("SQL 입문", loadedBook.getTitle());
        assertEquals("저자B", loadedBook.getAuthor());
        assertFalse(loadedBook.isAvailable(), "대출 중 상태(false)가 유지되어야 합니다.");
        assertEquals("admin", loadedBook.getBorrowerId());
    }

    @Test
    @DisplayName("DB로부터 사용자 데이터 로드 테스트 (loadUsers)")
    void loadUsers() {
        // When: 로드 실행 (이제 단일 User 객체를 반환함)
        User user = repository.loadUser("admin", "1111");

        // Then: 데이터 검증
        // 1. 객체가 null이 아닌지 확인 (조회 성공 여부)
        assertNotNull(user, "조회된 사용자 객체는 null일 수 없습니다.");

        // 2. ID가 일치하는지 확인 (기존의 stream().anyMatch()를 대체)
        assertEquals("admin", user.getUserId(), "조회된 ID가 'admin'이어야 합니다.");

        // 3. 권한(Type)도 맞는지 확인해보면 좋습니다.
        assertEquals("ADMIN", user.getRole(), "사용자 권한이 'ADMIN'이어야 합니다.");
    }
}