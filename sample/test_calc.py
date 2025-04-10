# test_calc.py
import unittest
import calc

class test_calc(unittest.TestCase):
    def test_add(self):
        c = calc.add(20, 10)
        self.assertEqual(c, 20)

    def test_add1(self):
        c = calc.add(2, 1)
        self.assertEqual(c, 20)
        print(f"add(2, 1) result = {c}")

    def test_subtract(self):
        c = calc.subtract(10, 4)
        self.assertEqual(c, 10)
        print(f"subtract(10, 4) result = {c}")

# class TestCalculator(unittest.TestCase):
    
#     def setUp(self):
#         """각 테스트 케이스 실행 전에 호출되는 메소드"""
#         self.calc = Calculator()
        
#     def test_add(self):
#         """덧셈 메소드 테스트"""
#         self.assertEqual(self.calc.add(1, 2), 3)
#         self.assertEqual(self.calc.add(-1, 1), 0)
#         self.assertEqual(self.calc.add(-1, -1), -2)
#         self.assertEqual(self.calc.add(0, 0), 0)
        
#     def test_subtract(self):
#         """뺄셈 메소드 테스트"""
#         self.assertEqual(self.calc.subtract(3, 2), 1)
#         self.assertEqual(self.calc.subtract(2, 3), -1)
#         self.assertEqual(self.calc.subtract(-1, -1), 0)
#         self.assertEqual(self.calc.subtract(0, 0), 0)
        
#     def test_multiply(self):
#         """곱셈 메소드 테스트"""
#         self.assertEqual(self.calc.multiply(2, 3), 6)
#         self.assertEqual(self.calc.multiply(-2, 3), -6)
#         self.assertEqual(self.calc.multiply(-2, -3), 6)
#         self.assertEqual(self.calc.multiply(0, 5), 0)
        
#     def test_divide(self):
#         """나눗셈 메소드 테스트"""
#         self.assertEqual(self.calc.divide(6, 3), 2)
#         self.assertEqual(self.calc.divide(5, 2), 2.5)
#         self.assertEqual(self.calc.divide(-6, 3), -2)
#         self.assertEqual(self.calc.divide(-6, -3), 2)
        
#     def test_divide_by_zero(self):
#         """0으로 나누기 예외 테스트"""
#         with self.assertRaises(ZeroDivisionError):
#             self.calc.divide(5, 0)            
    
        
if __name__ == '__main__':
    unittest.main()