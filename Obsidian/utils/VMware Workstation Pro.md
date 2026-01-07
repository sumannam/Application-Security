
# 개요

- VMware Workstation Pro는 데스크톱 컴퓨터에서 가상 머신을 생성하고 실행할 수 있는 고급 가상화 소프트웨어이다.
- 주요 특징
	- **다양한 운영체제 지원**
		- Windows, Linux, macOS, FreeBSD 등 다양한 게스트 운영체제 지원
		- 32비트 및 64비트 운영체제 모두 지원
	- **고급 가상화 기능**
		- 3D 그래픽 가속화
		- 다중 CPU 및 다중 코어 지원
		- 최대 64GB RAM 할당 가능한 가상머신 생성
		- 가상 네트워크 및 네트워크 설정 커스터마이징
	- **스냅샷 기능**
		- 가상머신의 현재 상태를 저장하고 나중에 복원 가능
		- 소프트웨어 테스트나 시스템 구성 변경 시 안전망 제공
	- **클론 기능**
		- 기존 가상머신의 복사본 생성 (전체 클론 또는 연결 클론)
		- 다양한 설정으로 동일한 VM을 여러 개 생성 가능
	- **팀 협업 기능**
		- 가상머신 공유 및 원격 접속
		- 암호화된 가상머신 생성 및 관리


# OVF Import
## 개요
OVF(Open Virtualization Format)는 **가상머신의 이미지를 또 다른 가상머신으로 변화하는 툴**이다. 

보통은 VualBox로 포팅할 때 사용한다. 
참고로 변화할 때는 오랜 시간이 소요된다. ovftool은 VMware을 자동으로 설치하면 있다.
변환하는 방법은 윈도우의 cmd을 열어서 다음과 같이 입력하면 된다. 

**VMware가 설치된 경로 이동(참고사항)** 
ovftool.exe "{.vmx file path}" "{New file path}\{file name.ovf} 
입력 상세 내용은 아래 URL 참고: [OVFTool](https://www.vmware.com/support/developer/ovf/)

## OVF Import 방법
1. File → Open 선택한다.
	
2. 파일 형식 OVF 선택 후 해당 파일 선택한다.
	![](attachments/Pasted%20image%2020250316064515.png)


3. 가상 머신 이름 및 저장할 경로 선택 후 'Import' 선택
		
	![](attachments/Pasted%20image%2020250316064531.png)
		
	※ 'D:\VMware'는 설치 폴더 경로의 예
	**※ Import를 클릭한 후 “Failed to open OVF descriptor”를 나올 경우,**
	- 아래 '해결방법1'로 처리 이후에도 오류 시 저에게 연락주세요.
    - ovf가 아닌 다른 파일들을 다운로드 받아야 합니다(현재 문제의 이유를 모르는 상태입니다).

<aside> ✅ 해결방법1) ovf의 파일 경로가 모두 영어로 지정되도록 수정합니다 (경로에 한글폴더가 있으면 오류발생)

</aside>

# 네트워크 설정

# 개요

VMware 환경에서의 네트워크는 공인망, 사설망, 폐쇄망으로 구분할 수 있다.

- 공인망(Bridged)은 인터넷에 직접 연결된 네트워크로, 공인 IP 주소를 사용하여 외부와 자유로운 통신이 가능하다. VMware에서는 Bridge 네트워크 모드로 구성할 수 있으며, 외부와 직접 통신하기 때문에 보안에 특히 주의를 기울여야 한다.

- 사설망(NAT)은 내부에서만 사용되는 네트워크로, 192.168.x.x, 172.16.x.x, 10.x.x.x와 같은 사설 IP 주소를 사용한다. NAT를 통해 외부 통신이 가능하며, VMware에서는 NAT 네트워크 모드로 구성할 수 있다. 주로 내부 시스템들 간의 통신에 사용된다.

- 폐쇄망(Host-only)은 외부 네트워크와 완전히 분리된 네트워크이다. 보안이 매우 중요한 환경에서 사용되며, 외부 인터넷과 완전히 차단되어 있다. VMware에서는 Host-only 네트워크 모드로 구성할 수 있으며, 중요한 데이터를 다루는 서버나 보안이 중요한 시스템에서 주로 사용된다.

| 구분                       | **External →**  <br> **Guest OS** | **Host OS →**  <br> **Guest OS** | **Guest OS →**  <br> **Guest OS** | **Guest OS**  <br>**인터넷** |
| ------------------------ | --------------------------------- | -------------------------------- | --------------------------------- | ------------------------- |
| Bridged  <br>**(공인망)**   | 가능                                | 가능                               | 가능                                | 가능                        |
| NAT  <br>**(사설망)**       | 불가능                               | 가능                               | 가능                                | 가능                        |
| Host-Only  <br>**(폐쇄망)** | 불가능                               | 가능                               | 가능                                | 불가능                       |

  

# VMware 네트워크 설정 방법

1. Edit → Virtual Network Editor로 이동한다.

	![](attachments/Pasted%20image%2020250316074311.png)
	    
		
2. Changed Settings를 클릭한다.
    
	![](attachments/Pasted%20image%2020250316074337.png)
		
		
3. VMware에서 네트워크 설정을 선택할 수 있다.
    
    ![](attachments/Pasted%20image%2020250316074352.png)	 
	
## 공인망(Bridged)

- 공인망(Bridged)은 인터넷에 직접 연결된 네트워크로, 공인 IP 주소를 사용하여 외부와 자유로운 통신이 가능하다. VMware에서는 Bridge 네트워크 모드로 구성할 수 있으며, 외부와 직접 통신하기 때문에 보안에 특히 주의를 기울여야 한다.

## 사설망(NAT)

### 개요

- 사설망(NAT)은 내부에서만 사용되는 네트워크로, 192.168.x.x, 172.16.x.x, 10.x.x.x와 같은 사설 IP 주소를 사용한다. NAT를 통해 외부 통신이 가능하며, VMware에서는 NAT 네트워크 모드로 구성할 수 있다. 주로 내부 시스템들 간의 통신에 사용된다.
 

### NAT 주소 설정 방법

1. NAT인 경우, IP 주소 3번째 자리 수를 맞추어야 한다. Subnet IP의 3번째 자리 수를 입력 후 Apply를 클릭하면 변경된다.
    
	![](attachments/Pasted%20image%2020250316074405.png)
    ※ Host-Only일 경우 위 그림 기준 3번째 자리는 `200`이다.
	 
	
2. IP주소 3번째 자리를 변경 후에는 에서 3번째 자리를 동일하게 맞춰야 한다.

  

## 폐쇄망(Host-only)

### 개요
- 폐쇄망(Host-only)은 외부 네트워크와 완전히 분리된 네트워크이다. 보안이 매우 중요한 환경에서 사용되며, 외부 인터넷과 완전히 차단되어 있다. VMware에서는 Host-only 네트워크 모드로 구성할 수 있으며, 중요한 데이터를 다루는 서버나 보안이 중요한 시스템에서 주로 사용된다.
  

### Host-only 주소 설정 방법

1. 폐쇄망 IP 주소 설정은 NAT에서의 IP 주소 설정과 동일하다.
    
    ![](attachments/Pasted%20image%2020250316074419.png)
    

# 가상머신에서 IP 설정 방법

## 가상머신에서 네트워크 설정 방법

1. VMware 화면에서 오른쪽 하단의 네트워크 아이콘 더블 클릭
	
	![](attachments/Pasted%20image%2020250316074432.png)	  
	
2. 설정 확인	    
	![](attachments/Pasted%20image%2020250316074449.png)
 

## 가상머신에서 IP 주소 변경 방법

1. `Activities` → `network` → `Network`를 실행한다.

	![](attachments/Pasted%20image%2020250316074458.png)
	
	
2. 설정 아이콘을 클릭한다.
	![](attachments/Pasted%20image%2020250316074507.png)
    
      
    
3. `IPv4`로 선택한 후, 아래 주소를 입력한다.
    
    > IPv4 Method
    > - Automatic : IP 주소가 DHCP로부터 작동으로 할당된다.
    > - Manual : 사용자가 수동으로 입력해야 한다.
    
    - Manual 선택 후, IP 주소 입력 예
```Bash
IPv4 Method : Manual
Address : 192.168.100.20
Netmast : 255.255.255.0
Gateway : 192.168.100.2
DNS : 168.126.63.1
```
![](attachments/Pasted%20image%2020250316074516.png)
          
    
4. 입력한 IP 주소를 적용한다.
		
	![](attachments/Pasted%20image%2020250316074527.png)
    
    ![](attachments/Pasted%20image%2020250316074538.png)
    
	
# 네트워크 진단 방법(4가지)

# **1. VMware Adapter 설정 확인**

1. VMware 화면에서 오른쪽 하단의 네트워크 아이콘 더블 클릭
	![](attachments/Pasted%20image%2020250316074556.png)
		  
	
2. 설정 확인
	![](attachments/Pasted%20image%2020250316074603.png)
    ※NAT와 Host-only의 IP 주소의 서브넷 번호 확인 방법은 아래 '3. IP 주소 확인'
	 
# **2. 외부 인터넷과의 연결 확인**

```Bash
$ ping 168.126.63.1
```

`정상 화면`
![](attachments/Pasted%20image%2020250316070018.png)

`오류 화면`
![](attachments/Pasted%20image%2020250316070029.png)
  

# **3. IP 주소 확인**

```Bash
$ ifconfig
```

  ![](attachments/Pasted%20image%2020250316070058.png)

NAT일 경우

| 192    | 168    | 100                                                                | 20                |
| ------ | ------ | ------------------------------------------------------------------ | ----------------- |
| 고정된 번호 | 고정된 번호 | Virtual Network Editor의 Subnet Address와 3번째 자리와 번호 일치 확인(아래 그림 확인) | 3~255까지 아무 번호나 가능 |
![](attachments/Pasted%20image%2020250316070117.png)
※ Host-Only일 경우 위 그림 기준 '200'임

  

# **4. IP 주소 변경**

1. `Activities` → `network` → `Network`를 실행한다.
    ![](attachments/Pasted%20image%2020250316070134.png)
    
    
2. 설정 아이콘을 클릭한다.
    ![](attachments/Pasted%20image%2020250316070142.png)
       
    
3. `IPv4`로 선택한 후, 아래 주소를 입력한다.
    
    ```Bash
    IPv4 Method : Manual
    Address : 192.168.100.20
    Netmast : 255.255.255.0
    Gateway : 192.168.100.2
    DNS : 168.126.63.1
    ```
	![](attachments/Pasted%20image%2020250316070205.png)
    
    > [!important] Host-Only일 경우, 외부와 단절되기 때문에 DNS Servers의 IP 주소 필요 없음
	
    
4. 입력한 IP 주소를 적용한다.
    ![](attachments/Pasted%20image%2020250316070225.png)
    ![](attachments/Pasted%20image%2020250316070232.png)