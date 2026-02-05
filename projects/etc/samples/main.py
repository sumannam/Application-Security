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