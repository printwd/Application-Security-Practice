import unittest
import time
from unittest.mock import patch, MagicMock
import sys
import os
from queue import Queue
import threading

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.ftp.attacks.ftp_bruteforce_multithreads import FTPBruteforcer

class TestFTPBruteforceMultithreads(unittest.TestCase):
    """FTP 무차별 대입 공격 도구의 멀티스레드 기능을 테스트하는 클래스"""
    
    def setUp(self):
        """각 테스트 실행 전에 실행되는 메소드"""
        self.test_host = 'localhost'
        self.test_usernames = ['user1', 'user2']
        self.test_passwords = ['pass1', 'pass2']
        self.bruteforcer = FTPBruteforcer(self.test_host)
    
    @patch('src.ftp.attacks.ftp_bruteforce_multithreads.FTP')
    def test_single_thread_login(self, mock_ftp):
        """단일 스레드 로그인 시도 테스트"""
        # FTP 모의 객체 설정
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value.__enter__.return_value = mock_ftp_instance
        
        # 로그인 시도
        result = self.bruteforcer.try_login('user1', 'pass1')
        
        # 결과 검증
        self.assertTrue(result)
        mock_ftp_instance.login.assert_called_once_with(user='user1', passwd='pass1')
    
    @patch('src.ftp.attacks.ftp_bruteforce_multithreads.FTP')
    def test_multithread_login(self, mock_ftp):
        """멀티스레드 로그인 시도 테스트"""
        # FTP 모의 객체 설정
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value.__enter__.return_value = mock_ftp_instance
        
        # 멀티스레드 공격 실행
        result = self.bruteforcer.bruteforce_attack(
            self.test_usernames,
            self.test_passwords,
            max_threads=2
        )
        
        # 결과 검증
        self.assertTrue(result)
        self.assertTrue(mock_ftp_instance.login.called)
    
    @patch('src.ftp.attacks.ftp_bruteforce_multithreads.FTP')
    def test_invalid_credentials(self, mock_ftp):
        """잘못된 자격 증명으로 인한 실패 테스트"""
        # FTP 모의 객체 설정 (로그인 실패 시뮬레이션)
        mock_ftp_instance = MagicMock()
        mock_ftp_instance.login.side_effect = Exception("Login failed")
        mock_ftp.return_value.__enter__.return_value = mock_ftp_instance
        
        # 로그인 시도
        result = self.bruteforcer.try_login('invalid', 'invalid')
        
        # 결과 검증
        self.assertFalse(result)
        mock_ftp_instance.login.assert_called_once_with(user='invalid', passwd='invalid')
    
    def test_progress_update(self):
        """진행률 표시 기능 테스트"""
        # 진행률 업데이트 테스트
        self.bruteforcer.attempts = 5
        self.bruteforcer.total_attempts = 10
        self.bruteforcer.start_time = time.time()
        
        # 진행률 업데이트 호출
        self.bruteforcer.update_progress()
        
        # 결과 검증
        self.assertEqual(self.bruteforcer.attempts, 6)  # 시도 횟수가 증가했는지 확인
    
    @patch('src.ftp.attacks.ftp_bruteforce_multithreads.FTP')
    def test_worker_thread(self, mock_ftp):
        """작업자 스레드 기능 테스트"""
        # FTP 모의 객체 설정
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value.__enter__.return_value = mock_ftp_instance
        
        # 테스트용 큐 생성
        credentials_queue = Queue()
        credentials_queue.put(('user1', 'pass1'))
        
        # 작업자 스레드 실행
        self.bruteforcer.worker(credentials_queue)
        
        # 결과 검증
        self.assertTrue(mock_ftp_instance.login.called)
        self.assertEqual(credentials_queue.qsize(), 0)  # 큐가 비어있는지 확인

if __name__ == '__main__':
    with open('src/ftp/attacks/ftp_bruteforce_multithreads.py', 'rb') as f:
        content = f.read().replace(b'\x00', b'')

    with open('src/ftp/attacks/ftp_bruteforce_multithreads.py', 'wb') as f:
        f.write(content)
    unittest.main() 