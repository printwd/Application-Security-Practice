import os
import sys
import unittest

from unittest.mock import patch
from io import StringIO

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ftp.main import print_menu, main

class testMain(unittest.TestCase):
    @patch('sys.argv', new=['main.py', '-H', '192.168.100.20', '-u', 'cju', '-p', 'security'])
    @patch('builtins.input', side_effect=['4'])
    def test_main_with_argv(self, mock_input):
        """!
        @fn         test_main_with_argv
        @brief      FTP 클라이언트 메인 함수 테스트
        @details    FTP 클라이언트 접속 후 메뉴를 출력하고 종료하는지 확인

        @param      mock_input   입력 모의 객체
        @return     None

        @author     남수만(sumannam@gmail.com)
        @date       2025.02.07
        """
        result = main()
        mock_input.assert_called()
        self.assertIsNone(result)
    

    @patch('builtins.input', side_effect=['192.168.100.20', 'cju', 'security', '4'])
    def test_main_with_input(self, mock_input):
        """!
        @fn         test_main_with_input
        @brief      입력 기반 메인 함수 테스트
        @details    사용자 입력으로 host, id, password를 받아 main() 함수 테스트

        @param      mock_input   입력 모의 객체 (host, id, pw, 메뉴선택)
        @return     None 

        @author     남수만(sumannam@gmail.com)
        @date       2025.02.07
        """
        result = main()
        mock_input.assert_called()
        self.assertEqual(mock_input.call_count, 4)  # 입력 4번 호출 확인
        self.assertIsNone(result)

    
    @patch('builtins.input', side_effect=[
    # 초기 연결 정보
    '192.168.100.20',   # FTP 서버 주소
    'cju',              # 사용자 이름
    'security',         # 비밀번호
    # 메뉴 선택들
    '1',               # 1. 파일 목록 보기
    '2',               # 2. 파일 업로드 실행
    '3',               # 3. 파일 다운로드 시도
    '1',               # 파일 선택 (1번 파일)
    '4'                # 4. 프로그램 종료
    ])
    def test_main_workflow(self, mock_input):
        """!
        @fn         test_main_workflow
        @brief      FTP 클라이언트 전체 워크플로우 테스트
        @details    1. FTP 연결 정보 입력 (서버주소, ID, PW)
                    2. 파일 목록 보기 테스트
                    3. 파일 업로드 테스트
                    4. 파일 다운로드 테스트
                    5. 프로그램 종료 테스트
        @param      mock_input   입력 모의 객체
        @return     None
        @author     사용자명(이메일)
        @date       2024.02.07
        """
        # 메인 함수 실행
        result = main()
        
        # 입력이 예상한 횟수만큼 호출되었는지 확인
        mock_input.assert_called()
        self.assertEqual(mock_input.call_count, 8)  # 총 8번의 입력이 있어야 함
        
        # 각 단계별 입력 프롬프트 확인
        actual_inputs = [call[0][0] for call in mock_input.call_args_list]
        expected_inputs = [
            'FTP 서버 주소: ',              # 초기 연결 정보
            '사용자 이름: ',
            '비밀번호: ',
            '메뉴를 선택하세요 (1-4): ',    # 파일 목록 보기
            '메뉴를 선택하세요 (1-4): ',    # 파일 업로드
            '메뉴를 선택하세요 (1-4): ',    # 파일 다운로드
            '\n파일 번호를 선택하세요 (0-1): ',  # 파일 선택
            '메뉴를 선택하세요 (1-4): '     # 종료
        ]
        
        # 실제 입력 프롬프트와 예상 프롬프트 비교
        for actual, expected in zip(actual_inputs, expected_inputs):
            self.assertEqual(actual, expected)
        
        # 메인 함수가 정상 종료되었는지 확인
        self.assertIsNone(result)