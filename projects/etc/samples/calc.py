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