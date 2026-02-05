import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.Collection;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class LibraryManagerTest {

    private LibraryManager manager;
    private LibraryRepository repository;
    private User currentUser;

    @BeforeEach
    void setUp() {
        // 테스트용 레포지토리와 매니저 초기화
        repository = new LibraryRepository();
        manager = new LibraryManager(repository);

        // 매니저 초기화 (파일 로드)
        manager.initialize();

        // 테스트를 위한 초기 데이터 강제 주입 (필요 시)
        // 실제 파일 없이 로직만 테스트하고 싶다면 Mock 객체를 사용하거나
        // 테스트용 도서를 직접 등록합니다.
        manager.getBookMap().clear();
        manager.addBook("테스트 자바", "저자A"); // ID: 1
    }

    @Test
    @DisplayName("로그인 성공 및 실패 테스트")
    void login() {
        // Given: users.csv에 admin/1111 데이터가 있다고 가정
        // When & Then
        assertTrue(manager.login("admin", "1111"), "관리자 로그인이 성공해야 합니다.");
        assertFalse(manager.login("admin", "wrong"), "비밀번호가 틀리면 실패해야 합니다.");
    }

    @Test
    @DisplayName("현재 로그인한 사용자 정보 확인")
    void getCurrentUser() {
        manager.login("admin", "1111");
        User user = manager.getCurrentUser();

        assertNotNull(user);
        assertEquals("admin", user.getUserId());
        assertTrue(user.isAdmin());
    }

    @Test
    @DisplayName("새로운 도서 등록 확인")
    void addBook() {
        int beforeSize = manager.getAllBooks().size();
        manager.addBook("새로운 책", "새로운 저자");

        assertEquals(beforeSize + 1, manager.getAllBooks().size());

        int target_id = manager.getBookCount();
        Book book = manager.getBookMap().get(target_id);
        assertEquals("새로운 책", book.getTitle());
    }

    @Test
    @DisplayName("도서 삭제 확인")
    void deleteBook() {
        // ID 1번 도서 삭제
        int target_id = manager.getBookCount();
        boolean result = manager.deleteBook(target_id);

        assertTrue(result);
        assertNull(manager.getBookMap().get(target_id));
    }

    /**
     * LibraryManager의 보안 취약점을 검증하기 위한 테스트 클래스입니다.
     * <p>주로 인증 로직 및 사용자 권한 제어와 관련된 취약점을 다룹니다.</p>
     * * @author Suman Nam
     * @see LibraryManager#login(String, String)
     *
     * @see <a href="https://github.com/sumannam/Java/issues/44">Issue #44: 보안 취약점 관련 단위 테스트 개발</a>
     */
    @Test
    @DisplayName("도서 대출 로직 확인")
    void borrowBook() {
        manager.login("user", "2222"); // 대출자 로그인

        // 성공 케이스
        int target_id = manager.getBookCount();
        boolean success = manager.borrowBook(target_id);
        assertTrue(success);
        assertFalse(manager.getBookMap().get(target_id).isAvailable());
        assertEquals("user", manager.getBookMap().get(target_id).getBorrowerId());

        // 실패 케이스 (이미 대출 중인 도서)
        boolean fail = manager.borrowBook(1);
        assertFalse(fail);
    }

    @Test
    @DisplayName("도서 반납 로직 확인")
    void returnBook() {
        manager.login("user", "2222");
        manager.borrowBook(1); // 먼저 대출

        // 반납 실행
        int target_id = manager.getBookCount();
        manager.borrowBook(target_id);

        boolean result = manager.returnBook(target_id);
        assertTrue(result);
        assertTrue(manager.getBookMap().get(target_id).isAvailable());
        assertEquals("null", manager.getBookMap().get(target_id).getBorrowerId());
    }

    @Test
    @DisplayName("키워드 기반 도서 검색 확인")
    void searchBook() {
        manager.addBook("파이썬 입문", "저자B");

        List<Book> results = manager.searchBook("자바");
        assertEquals(1, results.size());
        assertEquals("테스트 자바", results.get(0).getTitle());
    }

    @Test
    @DisplayName("전체 도서 목록 반환 확인")
    void getAllBooks() {
        Collection<Book> books = manager.getAllBooks();
        assertNotNull(books);
        assertFalse(books.isEmpty());
    }

    /**
     * SQL Injection 공격을 이용한 인증 우회 가능 여부를 테스트합니다.
     * <p><b>공격 시나리오:</b> 비밀번호를 모르는 상태에서 아이디 입력란에
     * 항상 참이 되는 조건({@code ' OR 1=1})을 주입하여 로그인을 시도합니다.</p>
     * * <p><b>예상 결과:</b> 취약한 코드 환경에서는 SQL 문법이 왜곡되어
     * 실제 비밀번호 일치 여부와 상관없이 로그인이 성공(true)해야 합니다.</p>
     *
     * * @see <a href="https://owasp.org/www-community/attacks/SQL_Injection">OWASP: SQL Injection</a>
     *
     * @see <a href="https://github.com/sumannam/Java/issues/40">Issue #40: SQL Injection 취약점 개발</a>
     */
    @Test
    @DisplayName("보안 테스트: SQL Injection을 이용한 인증 우회")
    void loginSqlInjectionTest() {
        // Given: 패스워드를 모르는 상태에서 항상 참이 되는 조건 주입
        String attackId = "' OR 1=1 #";
        String attackPw = "wrong_password";

        // When: 취약한 login 메서드 호출
        boolean result = manager.login(attackId, attackPw);

        // Then: 로그인이 성공(true)한다면 SQL Injection 취약점이 존재함을 입증
        assertTrue(result, "취약점 발견: SQL Injection 페이로드로 인증이 우회되었습니다.");

        if (result) {
            System.out.println("[경고] SQL Injection 공격 성공: 유효하지 않은 계정으로 로그인되었습니다.");
        }
    }

    /**
     * 운영체제 명령어 주입(OS Command Injection) 취약점의 존재 여부를 검증하는 테스트입니다.
     * * <p><b>테스트 목적:</b></p>
     * <ul>
     * <li>사용자 입력값이 OS 명령어의 인자로 전달될 때, 적절한 필터링이 부재할 경우 발생하는 위험성을 확인합니다.</li>
     * <li>명령어 구분자(&&, ;, |)를 통해 원래 의도하지 않은 추가 명령어가 실행될 수 있음을 증명합니다.</li>
     * </ul>
     *
     * <p><b>공격 시나리오:</b></p>
     * <ol>
     * <li>정상적인 IP 주소 뒤에 윈도우 명령어 구분자 {@code &&}와 파일 생성 명령어 {@code echo hacked > vuln.txt}를 결합합니다.</li>
     * <li>취약한 {@link LibraryManager#checkServerStatus(String)} 메소드에 해당 페이로드를 전달합니다.</li>
     * <li>명령어 주입이 성공하면, 서버의 현재 작업 디렉토리에 {@code vuln.txt} 파일이 생성됩니다.</li>
     * </ol>
     *
     * <p><b>보안 판정 기준:</b></p>
     * <ul>
     * <li>{@code assertTrue(isVulnerable)}: 테스트가 통과(Pass)하면 시스템에 <b>치명적인 보안 취약점</b>이 존재함을 의미합니다.</li>
     * <li>파일 생성에 성공했다면, 이는 공격자가 서버에서 임의의 코드를 실행하거나 데이터를 파괴할 수 있는 상태임을 입증합니다.</li>
     * </ul>
     *
     * @author Suman Nam
     * @see LibraryManager#checkServerStatus(String)
     * @see <a href="https://cwe.mitre.org/data/definitions/78.html">CWE-78: OS Command Injection</a>
     *
     * @see <a href="https://github.com/sumannam/Java/issues/43">Issue #43: OS Command Injection 취약점 개발</a>
     */
    @Test
    @DisplayName("보안 테스트: OS Command Injection을 통한 임의 파일 생성")
    void osCommandInjectionTest() {
        // Given: 핑 명령어 뒤에 'vuln.txt' 파일을 만드는 명령어를 삽입 (Windows 기준)
        String fileName = "vuln.txt";
        String payload = "127.0.0.1 && echo hacked > " + fileName;

        // When: 취약한 서버 진단 기능 실행
        manager.checkServerStatus(payload);

        // Then: 주입된 명령어(echo hacked > vuln.txt)가 실행되어 파일이 생성되었는지 확인
        File injectedFile = new File(fileName);
        boolean isVulnerable = injectedFile.exists();

        // 테스트 완료 후 생성된 파일 삭제 (흔적 제거)
        if (isVulnerable) {
            injectedFile.delete();
        }

        assertTrue(isVulnerable, "취약점 발견: OS 명령어가 주입되어 임의의 파일이 생성되었습니다.");

        if (isVulnerable) {
            System.out.println("[경고] OS Command Injection 공격 성공: 서버 내에서 임의 명령어가 실행되었습니다.");
        }
    }
}