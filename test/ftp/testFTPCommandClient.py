import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class TestFTPCommandClient(unittest.TestCase):
    """FTP 명령어 기반 클라이언트 테스트"""
    @patch('builtins.input', side_effect=[
    # 초기 연결 정보
    '192.168.100.20', 'cju', 'security',
    # FTP 명령어 시퀀스
    'cd /',               # 루트 디렉토리로 이동
    'get etc/passwd D:\\Git\\Application-Security\\test\\ftp\\passwd',  # 절대 경로로 지정
    'quit'                # 종료
    ])
    def test_download_passwd_file(self, mock_input):
        """!
        @fn         test_download_passwd_file
        @brief      /etc/passwd 파일 다운로드 테스트
        @details    1. 루트 디렉토리로 이동
                    2. /etc/passwd 파일을 지정된 경로에 다운로드
                    3. 파일 존재 여부 확인
        @param      mock_input   입력 모의 객체
        @return     None
        @author     사용자명(이메일)
        @date       2024.02.07
        """
        target_path = "D:\\Git\\Application-Security\\test\\ftp\\passwd"
        
        # 테스트 실행 전 파일이 있다면 삭제
        if os.path.exists(target_path):
            os.remove(target_path)
            
        # FTP 클라이언트 실행
        from ftp.attacks.ftp_command_client import main
        main()
        
        # 파일이 다운로드 되었는지 확인
        self.assertTrue(os.path.exists(target_path))
        
        # 파일 내용 확인
        with open(target_path, 'r') as f:
            content = f.read()
            self.assertIn('root:', content)  # passwd 파일 형식 확인
        
        # 테스트 후 파일 정리
        # os.remove(target_path)

if __name__ == '__main__':
   unittest.main()