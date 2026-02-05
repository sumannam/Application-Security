import sys
import os
import argparse
from typing import List

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.ftp.client.FTPClient import FTPClient

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

def main():
    # 커맨드 라인 인자 파싱
    host, user, password = parse_arguments()
    
    # FTP 클라이언트 인스턴스 생성
    client = FTPClient(host, user, password)

    # 서버 연결
    if not client.connect():
        print("프로그램을 종료합니다.")
        return

    try:
        while True:
            choice = print_menu()

            if choice == "1":
                print("\n=== 파일 목록 ===")
                files = client.list_files()
                if files:
                    for file in files:
                        print(file)
                else:
                    print("파일이 없거나 목록을 가져올 수 없습니다.")

            elif choice == "2":
                # 지정된 파일 업로드
                local_path = "D:\\Git\\Application-Security\\src\\ftp\\insecure\\application_security.txt"
                if not os.path.exists(local_path):
                    print(f"\n{local_path} 파일이 존재하지 않습니다.")
                    continue
                    
                print(f"\n{local_path} 파일을 업로드합니다...")
                client.upload_file(local_path)

            elif choice == "3":
                # 파일 목록 가져오기
                files = client.get_simple_file_list()
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
                client.download_file(remote_file, local_path)

            elif choice == "4":
                print("\n프로그램을 종료합니다.")
                break

            else:
                print("\n잘못된 선택입니다. 다시 선택해주세요.")

    finally:
        client.disconnect()

def parse_arguments() -> tuple:
    """커맨드 라인 인자 파싱"""
    parser = argparse.ArgumentParser(description='FTP Client for Security Testing')
    parser.add_argument('-H', '--host', help='FTP server host')
    parser.add_argument('-u', '--user', help='FTP username')
    parser.add_argument('-p', '--password', help='FTP password')
    parser.add_argument('-U', '--userlist', help='사용자명 리스트 파일')
    parser.add_argument('-P', '--passlist', help='비밀번호 리스트 파일')
    parser.add_argument('-d', '--delay', help='지연 시간 (무시됨)', type=float)
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
    # 입력 인자와 함께 메인 함수 실행
    # python main.py --host 192.168.100.20 --user cju --password security

    main()