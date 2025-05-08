"""
FTP 서버의 무차별 대입 공격(brute force attack) 방지 기능을 테스트하는 모듈

이 모듈은 다음과 같은 보안 기능을 테스트합니다:
1. 최대 로그인 시도 횟수 제한
2. 로그인 실패 시 대기 시간 증가
3. 일정 시간 후 로그인 시도 카운터 초기화

테스트 케이스:
- test_first_login_attempt: 첫 번째 로그인 시도 테스트
- test_consecutive_login_failures: 연속된 로그인 실패 테스트
- test_login_failures_with_time_progression: 시간 경과에 따른 로그인 실패 처리 테스트
- test_lockout_period_reset: 잠금 기간 이후 로그인 시도 카운터 리셋 테스트
"""

import unittest
import time
from unittest.mock import patch, MagicMock
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

import src.ftp.secure_main  # 전체 모듈을 임포트

class TestSecureMain(unittest.TestCase):
    """FTP 서버의 보안 기능을 테스트하는 클래스"""
    
    def setUp(self):
        """
        각 테스트 실행 전에 실행되는 메소드
        테스트 환경을 초기화하고 필요한 설정을 수행합니다.
        
        주요 작업:
        1. login_attempts 딕셔너리 초기화
        2. 테스트에 사용할 IP 주소 설정
        """
        # 전역 모듈 변수 직접 초기화
        src.ftp.secure_main.login_attempts = {}
        self.test_ip = '192.168.100.20'  # 모든 테스트에서 고정 IP 사용
    
    def test_first_login_attempt(self):
        """
        첫 번째 로그인 시도 테스트
        
        테스트 내용:
        1. 첫 로그인 시도는 항상 허용되어야 함
        2. 대기 시간이 0이어야 함
        3. IP 주소가 login_attempts에 기록되어야 함
        4. 시도 횟수가 1이어야 함
        """
        # 로그인 시도
        allowed, wait_time = src.ftp.secure_main.check_brute_force(self.test_ip)
        
        # 테스트 검증
        self.assertTrue(allowed)  # 로그인이 허용되어야 함
        self.assertEqual(wait_time, 0)  # 대기 시간이 0이어야 함
        self.assertIn(self.test_ip, src.ftp.secure_main.login_attempts)  # IP가 기록되어야 함
        self.assertEqual(len(src.ftp.secure_main.login_attempts[self.test_ip]), 1)  # 시도 횟수가 1이어야 함
    
    def test_consecutive_login_failures(self):
        """
        연속된 로그인 실패 테스트
        
        테스트 내용:
        1. MAX_ATTEMPTS(3번)까지는 로그인 시도가 허용되어야 함
        2. MAX_ATTEMPTS 초과 시도는 차단되어야 함
        3. 차단 시 대기 시간이 DELAY_FACTOR와 같아야 함
        """
        # MAX_ATTEMPTS 번까지 시도
        for i in range(1, src.ftp.secure_main.MAX_ATTEMPTS + 1):
            allowed, wait_time = src.ftp.secure_main.check_brute_force(self.test_ip)
            self.assertTrue(allowed)  # 허용되어야 함
            self.assertEqual(wait_time, 0)  # 대기 시간이 0이어야 함
            self.assertIn(self.test_ip, src.ftp.secure_main.login_attempts)  # IP가 기록되어야 함
            self.assertEqual(len(src.ftp.secure_main.login_attempts[self.test_ip]), i)  # 시도 횟수 확인
        
        # MAX_ATTEMPTS 초과 시도
        allowed, wait_time = src.ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)  # 차단되어야 함
        self.assertGreater(wait_time, 0)  # 대기 시간이 0보다 커야 함
        self.assertAlmostEqual(wait_time, src.ftp.secure_main.DELAY_FACTOR, delta=0.1)  # 대기 시간이 DELAY_FACTOR와 같아야 함
    
    @patch('time.time')
    def test_login_failures_with_time_progression(self, mock_time):
        """
        시간 경과에 따른 로그인 실패 처리 테스트
        
        테스트 내용:
        1. MAX_ATTEMPTS 초과 후 첫 번째 시도의 대기 시간 확인
        2. 대기 시간의 절반이 지난 후 다시 시도했을 때의 처리
        3. 충분한 시간이 지난 후 다시 시도 가능 여부 확인
        
        @patch 데코레이터: time.time() 함수를 모의(mock)하여 시간을 조작
        """
        # 시작 시간 설정
        current_time = 1000.0
        mock_time.return_value = current_time
        
        # MAX_ATTEMPTS 번 시도
        for _ in range(src.ftp.secure_main.MAX_ATTEMPTS):
            src.ftp.secure_main.check_brute_force(self.test_ip)
        
        # MAX_ATTEMPTS 초과 첫 번째 시도
        allowed, wait_time1 = src.ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)  # 차단되어야 함
        self.assertAlmostEqual(wait_time1, src.ftp.secure_main.DELAY_FACTOR, delta=0.1)  # 대기 시간 확인
        
        # 대기 시간의 절반만 경과
        mock_time.return_value = current_time + (wait_time1 / 2)
        
        # 다시 시도 - 여전히 차단되어야 함
        allowed, wait_time2 = src.ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)  # 차단 상태 유지
        
        # 두 번째 초과 시도에 대한 대기 시간 검사
        expected_wait_time = src.ftp.secure_main.DELAY_FACTOR * 2  # 대기 시간이 2배가 되어야 함
        self.assertAlmostEqual(wait_time2, expected_wait_time, delta=0.1)
        
        # 충분한 시간 경과 시뮬레이션 (LOCKOUT_TIME + 10초)
        mock_time.return_value = current_time + src.ftp.secure_main.LOCKOUT_TIME + 10
        
        # 다시 시도 - 이제 허용되어야 함
        allowed, _ = src.ftp.secure_main.check_brute_force(self.test_ip)
        self.assertTrue(allowed)  # 허용되어야 함
    
    @patch('time.time')
    def test_lockout_period_reset(self, mock_time):
        """
        잠금 기간 이후 로그인 시도 카운터 리셋 테스트
        
        테스트 내용:
        1. MAX_ATTEMPTS 번 시도 후
        2. LOCKOUT_TIME이 지난 후
        3. 다시 시도하면 첫 시도로 간주되어야 함
        
        @patch 데코레이터: time.time() 함수를 모의(mock)하여 시간을 조작
        """
        # 시작 시간 설정
        current_time = 3000.0
        mock_time.return_value = current_time
        
        # MAX_ATTEMPTS 번 시도
        for _ in range(src.ftp.secure_main.MAX_ATTEMPTS):
            src.ftp.secure_main.check_brute_force(self.test_ip)
        
        # LOCKOUT_TIME 이상 시간 경과 시뮬레이션
        mock_time.return_value = current_time + src.ftp.secure_main.LOCKOUT_TIME + 10
        
        # 다시 시도 - 카운터가 리셋되어 새로운 첫 시도로 간주되어야 함
        allowed, wait_time = src.ftp.secure_main.check_brute_force(self.test_ip)
        self.assertTrue(allowed)  # 허용되어야 함
        self.assertEqual(wait_time, 0)  # 대기 시간이 0이어야 함
        self.assertEqual(len(src.ftp.secure_main.login_attempts[self.test_ip]), 1)  # 시도 횟수가 1이어야 함

if __name__ == '__main__':
    unittest.main()