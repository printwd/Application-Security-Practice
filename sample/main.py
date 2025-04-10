# main.py
from calc import Calculator

def main():
    """계산기 클래스 사용 예제"""
    # 계산기 인스턴스 생성
    calc = Calculator()
    
    # 계산기 사용 예제
    print("===== 계산기 사용 예제 =====")
    
    # 덧셈
    num1, num2 = 10, 5
    result = calc.add(num1, num2)
    print(f"{num1} + {num2} = {result}")
    
    # 뺄셈
    result = calc.subtract(num1, num2)
    print(f"{num1} - {num2} = {result}")
    
    # 곱셈
    result = calc.multiply(num1, num2)
    print(f"{num1} * {num2} = {result}")
    
    # 나눗셈
    result = calc.divide(num1, num2)
    print(f"{num1} / {num2} = {result}")
    

if __name__ == "__main__":
    main()