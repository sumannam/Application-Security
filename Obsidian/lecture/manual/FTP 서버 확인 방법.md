
# 서버 구동 확인
	
1. 터미널을 연 후, Host OS와 통신 여부를 확인한다.
```
ping 192.168.100.1
```
![](attachments/Pasted%20image%2020250316072254.png)

> [!NOTE] 주의
> 네트워크에 문제가 발생할 경우, [VMware Workstation Pro](../../utils/VMware%20Workstation%20Pro.md)에서 네트워크 진단을 확인해야 한다.

2. IP를 확인한다.
	
	![](attachments/Pasted%20image%2020250316072328.png)

3. 서버 동작 여부를 아래 명령어로 확인한다.
```
sudo systemctl status vsftpd
```

![](attachments/Pasted%20image%2020250316072118.png)
	
	- `Ctrl + C`를 누르면 빠져 나온다.
	