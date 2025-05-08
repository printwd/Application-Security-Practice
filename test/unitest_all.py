import sys
import os
import psutil
import config
import subprocess

def test_build(file_name):
    """
    주어진 테스트 파일을 실행하는 함수
    
    Args:
        file_name (str): 실행할 테스트 파일의 상대 경로
    """
    try:
        # 현재 스크립트의 디렉토리 경로를 기준으로 파일 경로 구성
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_path = os.path.join(current_dir, file_name)
        
        result = subprocess.run(['python', test_file_path], check=True)
        print(f'{file_name} 빌드 성공')
    except subprocess.CalledProcessError:
        print(f'{file_name} 빌드 실패')

if __name__ == "__main__":
    # 상대 경로로 테스트 파일 지정
    test_build('unitest_ftp.py')
    # test_build('unitest_db.py')