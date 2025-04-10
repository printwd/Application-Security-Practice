# calc.py

    
def add( num1, num2):
    """두 숫자를 더하는 메소드"""
    return num1 + num2
    
def subtract( num1, num2):
    """두 숫자를 빼는 메소드"""
    return num1 - num2
    
def main():
    print("calc.py 모듈 실행")
    print(f"3 + 5 = {add(3, 5)}")
    print(f"10 - 4 = {subtract(10, 4)}")

if __name__ == "__main__":
     main()