import sys
import os
import argparse
import time
from typing import List, Dict, Tuple

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.ftp.client.FTPClient import FTPClient

# 로그인 시도 추적을 위한 글로벌 변수
login_attempts: Dict[str, List[float]] = {}
MAX_ATTEMPTS = 3  # 최대 로그인 시도 횟수
LOCKOUT_TIME = 300  # 잠금 시간(초)
DELAY_FACTOR = 2  # 실패 시 지연 시간 증가 계수
MAX_LOGIN_TRIES = 3  # 사용자에게 허용할 총 로그인 시도 횟수

def check_brute_force(ip):
    # global login_attempts
    
    current_time = time.time()
    
    # IP가 dictionary에 없으면 초기화
    if ip not in login_attempts:
        login_attempts[ip] = []
    
    # 시간 초과 여부 확인 - LOCKOUT_TIME이 지났으면 시도 초기화
    if login_attempts[ip] and (current_time - login_attempts[ip][0] > LOCKOUT_TIME):
        login_attempts[ip] = []
    
    # 현재 시도 시간 추가
    login_attempts[ip].append(current_time)
    
    # 시도 횟수가 MAX_ATTEMPTS를 초과하면 차단
    if len(login_attempts[ip]) > MAX_ATTEMPTS:
        # 대기 시간 계산 (지수적 증가)
        wait_time = DELAY_FACTOR * (len(login_attempts[ip]) - MAX_ATTEMPTS)
        return False, wait_time
    
    return True, 0

def attempt_login() -> Tuple[bool, FTPClient]:
    """
    로그인 시도 함수
    - 성공: (True, client 객체)
    - 실패: (False, None)
    """
    # 커맨드 라인 인자 파싱
    host, user, password = parse_arguments()
    
    # FTP 클라이언트 인스턴스 생성
    client = FTPClient(host, user, password)
    
    # 브루트 포스 방지 검사
    allowed, wait_time = check_brute_force(host)
    
    if not allowed:
        print(f"\n보안 경고: 너무 많은 로그인 시도가 감지되었습니다.")
        print(f"{wait_time:.1f}초 후에 다시 시도해주세요.")
        return False, None
    
    # 연결 시도
    connection_result = client.connect()
    
    # 연결 실패 시 지연 시간 추가 (브루트 포스 방지)
    if not connection_result:
        print("\n연결에 실패했습니다. 사용자 이름과 비밀번호를 확인해주세요.")
        delay = min(len(login_attempts.get(host, [])), 5)
        if delay > 0:
            print(f"보안을 위해 {delay}초 동안 대기합니다...")
            time.sleep(delay)
        return False, None
    else:
        # 성공 시 로그인 시도 초기화
        if host in login_attempts:
            del login_attempts[host]
        return True, client

def main():
    login_tries = 0
    connected_client = None
    
    # 최대 로그인 시도 횟수만큼 로그인 시도
    while login_tries < MAX_LOGIN_TRIES and connected_client is None:
        login_tries += 1
        success, client = attempt_login()
        
        if success:
            connected_client = client
            break
        elif login_tries < MAX_LOGIN_TRIES:
            print(f"\n로그인 시도 {login_tries}/{MAX_LOGIN_TRIES} 실패. 다시 시도해주세요.")
            continue
        else:
            print(f"\n최대 로그인 시도 횟수({MAX_LOGIN_TRIES}회)를 초과했습니다.")
            print("프로그램을 종료합니다.")
            return

    # 로그인 실패로 종료
    if connected_client is None:
        return
        
    try:
        while True:
            choice = print_menu()

            if choice == "1":
                print("\n=== 파일 목록 ===")
                files = connected_client.list_files()
                if files:
                    for file in files:
                        print(file)
                else:
                    print("파일이 없거나 목록을 가져올 수 없습니다.")

            elif choice == "2":
                # 지정된 파일 업로드
                local_path = "D:\\Git\\Application-Security\\ftp\\insecure\\application_security.txt"
                if not os.path.exists(local_path):
                    print(f"\n{local_path} 파일이 존재하지 않습니다.")
                    continue
                    
                print(f"\n{local_path} 파일을 업로드합니다...")
                connected_client.upload_file(local_path)

            elif choice == "3":
                # 파일 목록 가져오기
                files = connected_client.get_simple_file_list()
                if not files:
                    print("\n다운로드할 수 있는 파일이 없습니다.")
                    continue

                # 파일 선택하기
                file_choice = show_file_list_menu(files)
                if file_choice == 0:
                    continue

                # 선택한 파일 다운로드
                remote_file = files[file_choice - 1]
                # d:\ 경로에 다운로드
                local_path = "d:\\" + remote_file
                print(f"\n{remote_file} 파일을 {local_path}로 다운로드합니다...")
                connected_client.download_file(remote_file, local_path)

            elif choice == "4":
                print("\n프로그램을 종료합니다.")
                break

            else:
                print("\n잘못된 선택입니다. 다시 선택해주세요.")

    finally:
        if connected_client:
            connected_client.disconnect()

def print_menu():
    """메인 메뉴 출력"""
    print("\n=== FTP 클라이언트 메뉴 ===")
    print("1. 파일 목록 보기")
    print("2. 파일 업로드")
    print("3. 파일 다운로드")
    print("4. 종료")
    print("========================")
    return input("메뉴를 선택하세요 (1-4): ")

def show_file_list_menu(files: List[str]) -> int:
    """파일 목록을 보여주고 선택받기"""
    print("\n=== 다운로드할 파일을 선택하세요 ===")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print("0. 취소")
    
    while True:
        try:
            choice = int(input("\n파일 번호를 선택하세요 (0-{0}): ".format(len(files))))
            if 0 <= choice <= len(files):
                return choice
            print("잘못된 선택입니다.")
        except ValueError:
            print("숫자를 입력해주세요.")

def parse_arguments() -> tuple:
    """커맨드 라인 인자 파싱"""
    parser = argparse.ArgumentParser(description='FTP Client for Security Testing')
    parser.add_argument('-H', '--host', help='FTP server host')
    parser.add_argument('-u', '--user', help='FTP username')
    parser.add_argument('-p', '--password', help='FTP password')
    parser.add_argument('-U', '--userlist', help='사용자명 리스트 파일')
    parser.add_argument('-P', '--passlist', help='비밀번호 리스트 파일')
    parser.add_argument('-d', '--delay', help='로그인 실패 시 지연 시간(초)', type=float, default=1.0)
    args = parser.parse_args()
    
    # 입력 인자가 하나라도 있는지 확인
    has_args = any([args.host, args.user, args.password, args.userlist, args.passlist])
    
    if has_args:
        # 인자가 있는 경우 해당 값 사용
        host = args.host if args.host else "192.168.100.20"
        if args.userlist or args.passlist:  # 워드리스트 모드
            base_path = os.path.dirname(os.path.abspath(__file__))
            userlist_file = os.path.join(base_path, args.userlist) if args.userlist else None
            passlist_file = os.path.join(base_path, args.passlist) if args.passlist else None
            user = userlist_file if args.userlist else (args.user if args.user else "cju")
            password = passlist_file if args.passlist else (args.password if args.password else "security")
        else:  # 일반 모드
            user = args.user if args.user else "cju"
            password = args.password if args.password else "security"
    else:
        # 인자가 없는 경우 사용자 입력 받기
        print("\n=== FTP 연결 정보 입력 ===")
        host = input("FTP 서버 주소: ").strip() or "192.168.100.20"
        user = input("사용자 이름: ").strip() or "cju"
        password = input("비밀번호: ").strip() or "security"
    
    return host, user, password


if __name__ == "__main__":
    main()