
# 개요

- 테스트란 소프트웨어가 요구사항에 의해 개발된 산출물이 요구사항과 부합하는지 여부를 검증하기 위한 작업이다.
- 단위 테스트란 모듈 또는 응용 프로그램 내의 개별 코드 단위가 예상대로 작동하는지 확인하는 반복 가능한 활동이다.

# 유닛테스트(unittest)

- Python에 포함된 다양한 테스트를 자동화할 수 있는 기능이 포함되어 있는 표준 라이브러리
- unittest에 포함된 주요 개념
    - 테스트케이스(TestCase)
        - unittest 프레임 워크의 테스트 조직의 기본 단위
    - 픽스처(Fixture)
        - 테스트 함수의 전 또는 후에 실행
        - 테스트가 실행되기 전에 테스트 환경이 예상 된 상태에 있는지 확인하는 데 사용
        - 테스트 전에 데이터베이스 테이블을 만들거나 테스트 후에 사용한 리소스를 정리하는데 사용
    - 어서션(assertion)
        - unittest가 테스트가 통과하는지 또는 실패 하는지를 결정
        - bool test, 객체의 적합성, 적절한 예외 발생 등 다양한 점검할 수 있음
        - assertion이 실패하면 테스트 함수가 실패함

## 기본 구조

```python
import unittest

# TestCase를 작성
classCustomTests(unittest.TestCase):
	def test_runs(self):
	  """단순 실행여부 판별하는 테스트 메소드"""
		custom_function()

# unittest를 실행
if __name__ == '__main__':
    unittest.main()
```

- `test.py` 파일을 만들고, 코드를 아래와 같이 작성한다.
-  `TestCase` 를 작성하기 위해 `unittest.TestCase`를 상속한 테스트 클래스를 작성한다.
- `test_` 라는 이름으로 시작하는 메소드는 모두 테스트 메소드가 된다.
- `test_run()` 메소드는 단순 실행여부만 판별한다.
- `unittest.main()` 코드를 통해 테스트가 수행한다.


## assert 메소드 목록

### 기본 비교 메소드

```python
assertEqual(a, b, msg=None)         # a == b
assertNotEqual(a, b, msg=None)      # a != b
assertTrue(x, msg=None)             # bool(x) is True
assertFalse(x, msg=None)            # bool(x) is False
assertIs(a, b, msg=None)            # a is b
assertIsNot(a, b, msg=None)         # a is not b
assertIsNone(x, msg=None)           # x is None
assertIsNotNone(x, msg=None)        # x is not None
```

### 수치 비교 메소드 

```python
assertAlmostEqual(a, b, places=7, msg=None, delta=None)      # round(a-b, places) == 0
assertNotAlmostEqual(a, b, places=7, msg=None, delta=None)   # round(a-b, places) != 0
assertGreater(a, b, msg=None)       # a > b
assertGreaterEqual(a, b, msg=None)  # a >= b
assertLess(a, b, msg=None)          # a < b
assertLessEqual(a, b, msg=None)     # a <= b
```

### 이진 내용 관련 메소드

```python
assertMultiLineEqual(a, b, msg=None)    # 멀티라인 문자열 비교
assertSequenceEqual(a, b, msg=None)     # 시퀀스 비교
assertListEqual(a, b, msg=None)         # 리스트 비교
assertTupleEqual(a, b, msg=None)        # 튜플 비교
assertSetEqual(a, b, msg=None)          # 집합 비교
assertDictEqual(a, b, msg=None)         # 딕셔너리 비교
```

### 기타

```python

## 컨테이너 관련 메소드
assertIn(a, b, msg=None)            # a in b
assertNotIn(a, b, msg=None)         # a not in b
assertCountEqual(a, b, msg=None)    # a와 b가 같은 요소를 같은 개수만큼 포함 (순서 무관)

## 타입 관련 메소드
assertIsInstance(a, b, msg=None)    # isinstance(a, b)
assertNotIsInstance(a, b, msg=None) # not isinstance(a, b)

## 예외 관련 메소드
assertRaises(exception, callable, *args, **kwds)  # callable(*args, **kwds)가 exception을 발생
assertRaisesRegex(exception, regex, callable, *args, **kwds)  # exception 메시지가 regex와 일치
assertWarns(warning, callable, *args, **kwds)     # callable이 warning을 발생
assertWarnsRegex(warning, regex, callable, *args, **kwds)  # warning 메시지가 regex와 일치

## 로그 관련 메소드
assertLogs(logger=None, level=None)  # 로그 메시지를 캡처

## 정규식 관련 메소드
assertRegex(text, regex, msg=None)      # regex가 text와 일치
assertNotRegex(text, regex, msg=None)   # regex가 text와 일치하지 않음
```


# 활용 방법

## 기초 실습

1. 아래와 같이 소스 코드를 작성한다.
```python
# calc.py
def add(a, b):
    return a + b
 
def substract(a, b):
    return a - b
```

2. 소스 코드를 작성한다.
```python
import unittest
import calc
 
class test_calc(unittest.TestCase):
	def test_add(self):
		c = calc.add(20,10)
		self.assertEqual(c, 30)
 
if __name__ == '__main__':
    unittest.main()
```

> [!NOTE] 실습문제1
> 위 테스트 코드에 `test_sub()`를 만들어서 완성하시오.


## 기본 실습

### calc.py

```python
class Calculator:
    """기본적인 수학 연산을 수행하는 계산기 클래스"""
    
    def add(self, a, b):
        """두 숫자를 더하는 메소드"""
        return a + b
    
    def subtract(self, a, b):
        """두 숫자를 빼는 메소드"""
        return a - b
    
    def multiply(self, a, b):
        """두 숫자를 곱하는 메소드"""
        return a * b
    
    def divide(self, a, b):
        """두 숫자를 나누는 메소드
        
        Args:
            a: 분자
            b: 분모 (0이 아니어야 함)
            
        Returns:
            a / b의 계산 결과
            
        Raises:
            ZeroDivisionError: b가 0일 경우
        """
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return a / b
```

### main.py

```python
# main.py
from calc import Calculator

def main():
    """계산기 클래스 사용 예제"""
    # 계산기 인스턴스 생성
    calc = Calculator()
    
    # 계산기 사용 예제
    print("===== 계산기 사용 예제 =====")
    
    # 덧셈
    a, b = 10, 5
    result = calc.add(a, b)
    print(f"{a} + {b} = {result}")
    
    # 뺄셈
    result = calc.subtract(a, b)
    print(f"{a} - {b} = {result}")
    
    # 곱셈
    result = calc.multiply(a, b)
    print(f"{a} * {b} = {result}")
    
    # 나눗셈
    result = calc.divide(a, b)
    print(f"{a} / {b} = {result}")
    

if __name__ == "__main__":
    main()
```

### test_calc.py

```python
import unittest
from calc import Calculator

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        """각 테스트 케이스 실행 전에 호출되는 메소드"""
        self.calc = Calculator()
        
    def test_add(self):
        """덧셈 메소드 테스트"""
        self.assertEqual(self.calc.add(1, 2), 3)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)
        self.assertEqual(self.calc.add(0, 0), 0)
        
if __name__ == '__main__':
    unittest.main()
```

### 실행 방법

1. 터미널에서 경로를 변경하고 아래와 같이 실행한다.
```
cd sample
python test_calc.py
```


> [!NOTE] 실습문제2
> 위 테스트 코드에서 `뺄쎔 메소드 테스트`, `곱셈 메소드 테스트`, `나눗셈 메소드 테스트`를 각각 만드시오.


> [!NOTE] 실습문제3
> 위 테스트 코드에서 `0으로 나누기 예외 테스트`를 만드시오.

