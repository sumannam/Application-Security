import sys
import os
from ftplib import FTP, error_perm
from typing import List

class ftp_command_client:
    def __init__(self, host: str, user: str, passwd: str):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.ftp = None
        self.commands = {
            'ls': self.list_files,
            'dir': self.list_files,
            'cd': self.change_dir,
            'pwd': self.print_dir,
            'get': self.download_file,
            'put': self.upload_file,
            'help': self.show_help,
            'quit': self.quit,
            'exit': self.quit
        }

    def connect(self) -> bool:
        """FTP 서버 연결"""
        try:
            self.ftp = FTP(self.host)
            self.ftp.login(user=self.user, passwd=self.passwd)
            print(f"Connected to {self.host}")
            print(f"Current directory: {self.ftp.pwd()}")
            return True
        except error_perm as e:
            print(f"Connection failed: {str(e)}")
            return False

    def run_cli(self):
        """명령줄 인터페이스 실행"""
        if not self.connect():
            return

        print("\nType 'help' for commands, 'quit' to exit")
        while True:
            try:
                command = input('ftp> ').strip()
                if not command:
                    continue

                # 명령어와 인자 분리
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                if cmd in self.commands:
                    if self.commands[cmd](args) is False:
                        break
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")

            except error_perm as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"Error: {str(e)}")

    def list_files(self, args: List[str]) -> bool:
        """파일 목록 표시"""
        path = args[0] if args else '.'
        self.ftp.dir(path)
        return True

    def change_dir(self, args: List[str]) -> bool:
        """디렉토리 변경"""
        if not args:
            print("Usage: cd <directory>")
            return True
        
        self.ftp.cwd(args[0])
        print(f"Current directory: {self.ftp.pwd()}")
        return True

    def print_dir(self, args: List[str]) -> bool:
        """현재 디렉토리 표시"""
        print(f"Current directory: {self.ftp.pwd()}")
        return True

    def download_file(self, args: List[str]) -> bool:
        """파일 다운로드"""
        if not args:
            print("Usage: get <remote_file> [local_file]")
            return True

        remote_file = args[0]
        local_file = args[1] if len(args) > 1 else os.path.basename(remote_file)

        with open(local_file, 'wb') as f:
            self.ftp.retrbinary(f'RETR {remote_file}', f.write)
        print(f"Downloaded {remote_file} to {local_file}")
        return True

    def upload_file(self, args: List[str]) -> bool:
        """파일 업로드"""
        if not args:
            print("Usage: put <local_file> [remote_file]")
            return True

        local_file = args[0]
        remote_file = args[1] if len(args) > 1 else os.path.basename(local_file)

        if not os.path.exists(local_file):
            print(f"Local file not found: {local_file}")
            return True

        with open(local_file, 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_file}', f)
        print(f"Uploaded {local_file} to {remote_file}")
        return True

    def show_help(self, args: List[str]) -> bool:
        """도움말 표시"""
        print("\nAvailable commands:")
        print("  ls, dir           List files in current directory")
        print("  cd <path>         Change directory")
        print("  pwd               Show current directory")
        print("  get <remote> [local]  Download file")
        print("  put <local> [remote]  Upload file")
        print("  help              Show this help")
        print("  quit, exit        Exit program")
        return True

    def quit(self, args: List[str]) -> bool:
        """프로그램 종료"""
        if self.ftp:
            self.ftp.quit()
        print("Goodbye!")
        return False

def main():
    if len(sys.argv) > 1:
        # 명령줄 인자로 실행
        if len(sys.argv) != 4:
            print("Usage: ftpcmd.py <host> <user> <password>")
            return
        host, user, passwd = sys.argv[1:4]
    else:
        # 대화형으로 정보 입력
        print("=== FTP Connection Info ===")
        host = input("Host: ").strip() or "192.168.100.20"
        user = input("User: ").strip() or "cju"
        passwd = input("Password: ").strip() or "security"

    client = ftp_command_client(host, user, passwd)
    client.run_cli()

if __name__ == "__main__":
    main()