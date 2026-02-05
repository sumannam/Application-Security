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