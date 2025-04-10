# calc.py
class Calculator:
    """기본적인 수학 연산을 수행하는 계산기 클래스"""
    
    def add(self, num1, num2):
        """두 숫자를 더하는 메소드"""
        return num1 + num2
    
    def subtract(self, num1, num2):
        """두 숫자를 빼는 메소드"""
        return num1 - num2
    
    def multiply(self, num1, num2):
        """두 숫자를 곱하는 메소드"""
        return num1 * num2
    
    def divide(self, num1, num2):
        """두 숫자를 나누는 메소드
        
        Args:
            num1: 분자
            num2: 분모 (0이 아니어야 함)
            
        Returns:
            num1 / num2의 계산 결과
            
        Raises:
            ZeroDivisionError: num2가 0일 경우
        """
        if num2 == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return num1 / num2