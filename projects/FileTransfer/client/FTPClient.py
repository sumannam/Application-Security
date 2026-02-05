from ftplib import FTP, error_perm
import os
from typing import List

class FTPClient:
    def __init__(self, host: str, user: str, passwd: str):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.ftp = None

    def connect(self) -> bool:
        """FTP 서버에 연결"""
        try:
            self.ftp = FTP(self.host)
            self.ftp.login(user=self.user, passwd=self.passwd)
            print(f"Connected to {self.host}")
            print(f"Welcome message: {self.ftp.getwelcome()}")
            return True
        except error_perm as e:
            # FTP 서버의 응답 메시지를 그대로 출력
            if "530 Login incorrect" in str(e):
                print(f"Connection failed: 530 Login incorrect")
            elif "530 User not found" in str(e):
                print(f"Connection failed: 530 User not found")
            else:
                print(f"Connection failed: {str(e)}")
            return False
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def list_files(self, path: str = ".") -> List[str]:
        """현재 디렉토리의 파일 목록 조회"""
        try:
            files = []
            self.ftp.dir(path, files.append)
            return files
        except Exception as e:
            print(f"Error listing files: {str(e)}")
            return []

    def get_simple_file_list(self) -> List[str]:
        """파일 이름만 리스트로 반환 (폴더 제외)"""
        try:
            all_items = []
            self.ftp.dir(all_items.append)
            
            # 폴더를 제외하고 파일만 필터링 (첫 문자가 'd'인 경우 폴더)
            files = []
            for item in all_items:
                # FTP LIST 명령의 결과에서 첫 문자가 'd'가 아닌 경우만 파일
                if not item.startswith('d'):
                    # 파일명만 추출 (마지막 부분)
                    filename = item.split()[-1]
                    files.append(filename)
            
            return files
        except Exception as e:
            print(f"Error getting file list: {str(e)}")
            return []

    def upload_file(self, local_path: str, remote_path: str = None) -> bool:
        """파일 업로드"""
        try:
            if not os.path.exists(local_path):
                print(f"Local file {local_path} does not exist.")
                return False
                
            if remote_path is None:
                remote_path = os.path.basename(local_path)
                
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_path}', file)
            print(f"Successfully uploaded {local_path} to {remote_path}")
            return True
        except Exception as e:
            print(f"Upload failed: {str(e)}")
            return False

    def download_file(self, remote_path: str, local_path: str = None) -> bool:
        """파일 다운로드"""
        try:
            if local_path is None:
                local_path = os.path.basename(remote_path)
                
            with open(local_path, 'wb') as file:
                self.ftp.retrbinary(f'RETR {remote_path}', file.write)
            print(f"Successfully downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            print(f"Download failed: {str(e)}")
            return False

    def disconnect(self):
        """FTP 연결 종료"""
        if self.ftp:
            self.ftp.quit()
            print("Disconnected from FTP server")