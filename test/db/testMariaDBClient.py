import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))
from db.insecure.MariaDBClient import MariaDBClient

class testMariaDBClient(unittest.TestCase):
    """!
    @fn         testMariaDBClient
    @brief      MariaDB 클라이언트 연결 테스트
    @details    데이터베이스 연결 및 쿼리 실행 테스트
    @author     사용자명(이메일)
    @date       2024.02.07
    """

    def setUp(self):
        """테스트 설정"""
        self.client = MariaDBClient(
            host="192.168.100.20",
            user="root",
            password="security",
            database="cju"
        )

    def test_connection(self):
        """!
        @fn         test_connection
        @brief      데이터베이스 연결 테스트
        @details    MariaDB 서버 연결 확인
        """
        # 연결 시도
        result = self.client.connect()
        
        # 연결 성공 확인
        self.assertTrue(result)
        self.assertIsNotNone(self.client.connection)

    def tearDown(self):
        """테스트 정리"""
        if self.client:
            self.client.disconnect()