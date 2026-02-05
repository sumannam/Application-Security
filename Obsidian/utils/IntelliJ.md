# 개요

- IntelliJ IDEA는 JetBrains에서 개발한 자바 개발자를 위한 통합 개발 환경(IDE)
- 강력한 코드 분석, 지능형 코드 완성, 효율적인 리팩토링 도구를 제공하여 자바 개발 생산성을 높이는 데 중점을 둔 환경
- 주요 특징
    - 지능형 코드 완성 및 분석
    - 고급 디버깅 및 테스트 지원
    - 다양한 프레임워크 지원 (Spring, JavaFX, Android 등)
    - 강력한 버전 관리 시스템 통합
    - 확장 가능한 플러그인 에코시스템
    - Ultimate 버전과 무료 Community 버전 제공
- 상세 내용은 아래 URL 참고
       [https://namu.wiki/w/IntelliJ%20IDEA](https://namu.wiki/w/IntelliJ%20IDEA)
    

# 설치

1. 아래 URL를 접속한 후, 다운로드를 선택한다.
		[https://www.jetbrains.com/idea/](https://www.jetbrains.com/idea/)
        
	![](attachments/Pasted%20image%2020250316062256.png)
		
2. 다운로드 exe를 선택한 후, 파일을 저장한다.
	![](attachments/Pasted%20image%2020250316062249.png)
		 
3. 다운로드 파일을 설치한다.
    - 설치 첫 화면
	    
	 ![](attachments/Pasted%20image%2020250316062232.png)
		
    - 중간에 선택해야 할 화면
        
	    ![](attachments/Pasted%20image%2020250316062222.png)
	    ![](attachments/Pasted%20image%2020250316062217.png)
    
4. 바탕화면에 아래 아이콘이 생성되면 설치 성공이다.
	
	![](attachments/Pasted%20image%2020250316062204.png)

# 프로젝트 생성

## 새 프로젝트 생성

1. 바탕화면에 Intellij 아이콘을 클릭한다.
    
    - 최초 실행 시 Windows 보안 경고 화면이 나온다. `액세스 허용`을 선택한다.
        
        ![](attachments/Pasted%20image%2020250316062144.png)
        
    - VSCode가 설치되어 있을 경우, 아래 화면이 나온다. `Skip Import`를 선택한다.
        
        ![](attachments/Pasted%20image%2020250316062134.png)
        ![](attachments/Pasted%20image%2020250316062127.png)
    
2. `New Project`를 선택한다.
	
	![](attachments/Pasted%20image%2020250316062118.png)
		
3. 아래와 같이 입력한다.
		
	![](attachments/Pasted%20image%2020250316062107.png)
    
    - `Name` : 프로젝트의 이름을 입력하는 필드
    - `Location` : 프로젝트가 저장될 디렉토리 경로를 지정
    - `JDK`(Java Development Kit) : 프로젝트에서 사용할 자바 개발 키트 버전 선택
        - 개발 환경에 따라 다른 JDK 버전으로 추가 또는 변경 가능
    
4. 아래와 같이 프로젝트가 생성된다.
	![](attachments/Pasted%20image%2020250316062054.png)
    
## 소스 코드

### 기초 코드 분석
```Java
public class Main {
    public static void main(String[] args) {
        System.out.printf("Hello and welcome!");
        for (int i = 1; i <= 5; i++) {
            System.out.println("i = " + i);
        }
    }
}
```

- 클래스 선언: `public class Main`
    - Java에서는 모든 코드가 클래스 안에 포함 필요
        - 현재는 `Main`이라는 이름의 클래스 생성
    - 메인 메소드: `public static void main(String[] args)`
        - 프로그램의 시작점
        - Java 프로그램이 실행될 때 가장 먼저 이 메소드를 찾아 실행
        - 상세 설명하고 있음
    - 화면에 출력하기: `System.out.printf("Hello and welcome!");`
        - 화면에 "Hello and welcome!"이라는 메시지 출력
        - printf는 형식화된 텍스트를 출력하는 명령어

  

### 반복문 코드 분석

```Java
for (int i = 1; i <= 5; i++) {
    System.out.println("i = " + i);
}
```

- 1부터 5까지 숫자를 반복하는 루프(반복문)
    - `int i = 1`: i라는 변수를 1로 시작
    - `i <= 5`: i가 5 이하일 동안 반복
    - `i++`: 매번 반복 후에 i를 1씩 증가
    - 루프 안에서는 현재 i의 값을 "i = 숫자" 형태로 출력

## 소스 코드 실행
1. 프로젝트 실행은 아래처럼 2가지 방법이 있다.
    
    - `Shift` + `F10` 누르기
    - ▶️ 클릭
	![](attachments/Pasted%20image%2020250316062037.png)
    
2. 실행 결과를 확인한다.
	
	![](attachments/Pasted%20image%2020250316062027.png)

### 소스 코드 응용: args 설정
```Java
public class Main {    
	public static void main(String[] args) {        
		for(String arg: args)   {
			System.out.println(arg);        
		}    
	}
}
```

  

1. `…` → `Edit`를 선택한다.
	
	![](attachments/Pasted%20image%2020250316062012.png)
    
2. 아래와 같이 파라미터를 입력한 후, `Run`를 선택한다.
    ```Java
    a b "c d" e
    ```
		
	![](attachments/Pasted%20image%2020250316061957.png)
    
3. 실행 결과를 확인한다.
		
	![](attachments/Pasted%20image%2020250316061923.png)
    

# JetBrains 가입

## 일반 계정 생성

1. 아래 URL에 접속한 후 가입한다.
		
	[https://account.jetbrains.com/login](https://account.jetbrains.com/login)
	
	![](attachments/Pasted%20image%2020250316061931.png)
    

  

# 교육용 라이선스 발행

1. 아래 URL에 접속한다.
    [https://www.jetbrains.com/ko-kr/community/education/#students](https://www.jetbrains.com/ko-kr/community/education/#students)
    
	![](attachments/Pasted%20image%2020250316061755.png)

2. 회원 가입을 위해 아래를 입력한다. 입력할 때 학교 이메일을 입력한다.
    
	![](attachments/Pasted%20image%2020250316061818.png)
	
    
3. 가입 후 메일 인증을 받는다.
		
	![](attachments/Pasted%20image%2020250316061659.png)
    
4. 인증 받은 후 Student Pack Liense를 받는다(단, 라이센스는 1년에 한 번씩 갱신해야 한다).
    [https://account.jetbrains.com/licenses](https://account.jetbrains.com/licenses)
	![](attachments/Pasted%20image%2020250316061836.png)

5. IntelliJ에서 설정 버튼을 누른 후 Manage License를 선택한다.
	
	![](attachments/Pasted%20image%2020250316061640.png)
    
6. JetBrains의 계정을 입력한 후 라이센스를 구독한다.
	
	![](attachments/Pasted%20image%2020250316061633.png)
	![](attachments/Pasted%20image%2020250316061628.png)

