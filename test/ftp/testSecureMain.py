import unittest
import time
from unittest.mock import patch
import sys
import os

# secure_main 모듈을 직접 가져오기 위한 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ftp.secure_main  # 전체 모듈을 임포트

class testSecureMain(unittest.TestCase):
    
    def setUp(self):
        """각 테스트 실행 전에 login_attempts 딕셔너리 초기화"""
        # 전역 모듈 변수 직접 초기화
        ftp.secure_main.login_attempts = {}
        self.test_ip = '192.168.100.20'  # 모든 테스트에서 고정 IP 사용
    
    def test_first_login_attempt(self):
        """첫 번째 로그인 시도는 항상 허용되어야 함"""
        allowed, wait_time = ftp.secure_main.check_brute_force(self.test_ip)
        
        self.assertTrue(allowed)
        self.assertEqual(wait_time, 0)
        self.assertIn(self.test_ip, ftp.secure_main.login_attempts)
        self.assertEqual(len(ftp.secure_main.login_attempts[self.test_ip]), 1)
    
    def test_consecutive_login_failures(self):
        """연속된 로그인 실패 테스트"""
        # 먼저 IP 주소가 login_attempts에 존재하는지 확인하고, 각 반복에서 검증
        for i in range(1, ftp.secure_main.MAX_ATTEMPTS + 1):
            allowed, wait_time = ftp.secure_main.check_brute_force(self.test_ip)
            self.assertTrue(allowed)
            self.assertEqual(wait_time, 0)
            self.assertIn(self.test_ip, ftp.secure_main.login_attempts)  # 키 존재 확인
            self.assertEqual(len(ftp.secure_main.login_attempts[self.test_ip]), i)
        
        # MAX_ATTEMPTS 초과 시도
        allowed, wait_time = ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)
        self.assertGreater(wait_time, 0)
        self.assertAlmostEqual(wait_time, ftp.secure_main.DELAY_FACTOR, delta=0.1)
    
    @patch('time.time')
    def test_login_failures_with_time_progression(self, mock_time):
        """시간 경과에 따른 로그인 실패 처리 테스트"""
        # 시작 시간 설정
        current_time = 1000.0
        mock_time.return_value = current_time
        
        # MAX_ATTEMPTS 번 시도
        for _ in range(ftp.secure_main.MAX_ATTEMPTS):
            ftp.secure_main.check_brute_force(self.test_ip)
        
        # MAX_ATTEMPTS 초과 첫 번째 시도
        allowed, wait_time1 = ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)
        self.assertAlmostEqual(wait_time1, ftp.secure_main.DELAY_FACTOR, delta=0.1)
        
        # 대기 시간의 절반만 경과
        mock_time.return_value = current_time + (wait_time1 / 2)
        
        # 다시 시도 - 여전히 차단되어야 함
        allowed, wait_time2 = ftp.secure_main.check_brute_force(self.test_ip)
        self.assertFalse(allowed)
        
        # 두 번째 초과 시도에 대한 대기 시간 검사
        # 대기 시간은 DELAY_FACTOR * (초과 시도 횟수) = DELAY_FACTOR * 2가 되어야 함
        expected_wait_time = ftp.secure_main.DELAY_FACTOR * 2
        self.assertAlmostEqual(wait_time2, expected_wait_time, delta=0.1)
        
        # 충분한 시간 경과 시뮬레이션
        mock_time.return_value = current_time + ftp.secure_main.LOCKOUT_TIME + 10
        
        # 다시 시도 - 이제 허용되어야 함 (LOCKOUT_TIME 이후 시도는 카운터가 리셋됨)
        allowed, _ = ftp.secure_main.check_brute_force(self.test_ip)
        self.assertTrue(allowed)
    
    @patch('time.time')
    def test_lockout_period_reset(self, mock_time):
        """잠금 기간 이후 로그인 시도 카운터 리셋 테스트"""
        # 시작 시간 설정
        current_time = 3000.0
        mock_time.return_value = current_time
        
        # MAX_ATTEMPTS 번 시도
        for _ in range(ftp.secure_main.MAX_ATTEMPTS):
            ftp.secure_main.check_brute_force(self.test_ip)
        
        # LOCKOUT_TIME 이상 시간 경과 시뮬레이션
        mock_time.return_value = current_time + ftp.secure_main.LOCKOUT_TIME + 10
        
        # 다시 시도 - 카운터가 리셋되어 새로운 첫 시도로 간주되어야 함
        allowed, wait_time = ftp.secure_main.check_brute_force(self.test_ip)
        self.assertTrue(allowed)
        self.assertEqual(wait_time, 0)
        self.assertEqual(len(ftp.secure_main.login_attempts[self.test_ip]), 1)

if __name__ == '__main__':
    unittest.main()