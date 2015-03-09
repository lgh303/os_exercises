#lec 3 SPOC Discussion

## 第三讲 启动、中断、异常和系统调用-思考题

## 3.1 BIOS
 1. 比较UEFI和BIOS的区别
 	UEFI : Unified Extensible Firmware Interface 统一的可扩展固件接口
	UEFI像一个固化在主板上的小型操作系统，使用C语言开发，而不是汇编
	UEFI具备文件系统的支持，可以直接读取FAT分区中的文件，并可以执行（efi文件）
	UEFI的安全性较高，速度较快
 	
 2. 描述PXE的大致启动流程。
 	PXE ： Pre-boot Execution Environment
	1、BIOS启动，PXE Client程序（ROM中）进入内存，显示命令菜单
	2、PXE Client程序开始寻找网络引导程序
	3、引导程序读取配置文件，获得系统初始化到相关文件信息
	4、系统启动，开始进行安装

## 3.2 系统启动流程
 1. 了解NTLDR的启动流程。
 	NTLDR（NT Loader） 文件的是一个隐藏的，只读的系统文件，位置在系统盘的根目录，用来装载操作系统。
	1、电源自检程序开始运行
	2、主引导记录被装入内存，并且程序开始执行
	3、活动分区的引导扇区被装入内存
	4、NTLDR从引导扇区被装入并初始化
	5、将处理器的实模式改为32位平滑内存模式
	6、NTLDR开始运行适当的小文件系统驱动程序。
	7、NTLDR读boot.ini文件
	8、NTLDR装载所选操作系统
	9.Ntdetect搜索计算机硬件并将列表传送给NTLDR，以便将这些信息写进\\HKE Y_LOCAL_MACHINE\HARDWARE中。
	10.然后NTLDR装载Ntoskrnl.exe，Hal.dll和系统信息集合。
	11.Ntldr搜索系统信息集合，并装载设备驱动配置以便设备在启动时开始工作
	12.Ntldr把控制权交给Ntoskrnl.exe，这时,启动程序结束,装载阶段开始
 
 2. 了解GRUB的启动流程。
 	硬盘启动以后转向MBR，装载GRUB。GRUB再将控制权给实际操作系统

 3. 比较NTLDR和GRUB的功能有差异。
 	
 4. 了解u-boot的功能。

## 3.3 中断、异常和系统调用比较
 1. 举例说明Linux中有哪些中断，哪些异常？
 2. Linux的系统调用有哪些？大致的功能分类有哪些？  (w2l1)

 	答： Linux系统调用的大致数量上百个
		 分类：
				进程控制
				e.g.  fork： 创建一个新进程 
					  clone：按指定条件创建子进程
					  execve：运行可执行文件
					  exit：终止进程
					  getpid： 获取进程标示号
					  ....
			  	文件系统控制
				e.g.  文件读写控制
						open  打开文件
						creat
						close
						read
						write
						....
					  文件系统操作
						chdir
						chown：改变文件的属组或用户组
						stat：获取文件信息
						mount
						....
				系统控制
				e.g.  ioctl : I/O总控制函数
					  reboot：重新启动
					  sysinfo：取得系统信息
					  outb：低级端口操作
					  ....
				内存管理 : brk mlock mmap msync sync ...
				网络管理 : getdomainname gethostid gethostname ...
				socket控制 : bind connect accept send recv listen ...
				用户管理 : getuid getgid ...
				进程间通信 : ipc pipe ...
		 

```
  + 采分点：说明了Linux的大致数量（上百个），说明了Linux系统调用的主要分类（文件操作，进程管理，内存管理等）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```
 
 3. 以ucore lab8的answer为例，uCore的系统调用有哪些？大致的功能分类有哪些？(w2l1)

 	答： ucore 中系统调用有22个
	
	进程控制：	
    			exit
    			fork
    			getpid
    			exec
    			wait
				yield
    			kill
				sleep

	文件操作：
				open
    			close
    			read
    			write
    			seek
    			fstat
    			fsync
				putc
				pgdir
				getcwd
				getdirentry
				dup

	系统控制：
				gettime
				lab6_set_priority

	除此之外，ucore还可以增加网络管理&socket有关的系统调用，如gethostid, connect, send, accept等等，以增加网络功能。
    
    
 ```
  + 采分点：说明了ucore的大致数量（二十几个），说明了ucore系统调用的主要分类（文件操作，进程管理，内存管理等）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```
 
## 3.4 linux系统调用分析
 1. 通过分析[lab1_ex0](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex0.md)了解Linux应用的系统调用编写和含义。(w2l1)

 	答 ： 
	   对于所有的系统调用，系统调用号在%eax中。
	   对于小于六个参数的系统调用，参数依次存放在%ebx,%ecx,%edx,%esi,%edi中
	   系统调用的返回值保存在%eax中

		objdump：
				objdump命令是Linux下的反汇编目标文件或者可执行文件的命令
				可以以一种可阅读的格式让用户更多地了解二进制文件可能带有的附加信息
		nm：
				用来列出目标文件的符号清单				
		file：
				file是检测文件类型的命令，即文件组织的方式，通常不同的文件类型执行不同的标准

		代码解释：
		.include "defines.h"          // defines.h 中包含各个中断号
		.data	 					  // 数据段声明
		hello:
			.string "hello world\n"	  // hello为要输出的字符串

		.globl	main	   			  
		main:
			movl	$SYS_write,%eax	  //  %eax 中断号
			movl	$STDOUT,%ebx	  //  %ebx 第一个参数	输出流描述符
			movl	$hello,%ecx		  //  %ecx 第二个参数 起始地址
			movl	$12,%edx		  //  %edx 第三个参数 长度
			int	$0x80				  //  系统调用

			ret

 ```
  + 采分点：说明了objdump，nm，file的大致用途，说明了系统调用的具体含义
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 
 ```
 
 2. 通过调试[lab1_ex1](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex1.md)了解Linux应用的系统调用执行过程。(w2l1)

 	答： 
		strace : 跟踪系统调用和信号
		一个集诊断、调试、统计与一体的工具
		可以使用strace对应用的系统调用和信号传递的跟踪结果来对应用进行分析，以达到解决问题或者是了解应用工作过程的目的

		执行 strace ./lab1-ex1
		得到整个程序执行过程中所有到系统调用如下
			execve("./lab1-ex1", ["./lab1-ex1"], [/* 64 vars */]) = 0
			brk(0)                                  = 0x1ecc000
			access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
			mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f63b83ad000
			access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
			open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
			fstat(3, {st_mode=S_IFREG|0644, st_size=87791, ...}) = 0
			mmap(NULL, 87791, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f63b8397000
			......
			......
			write(1, "hello world\n", 12hello world)           = 12
			exit_group(12)                          = ?

		执行 strace -c ./lab1-ex1
		可以得到对所有系统调用的一个统计分析
				% time     seconds  usecs/call     calls    errors syscall
				 ------ ----------- ----------- --------- --------- ----------------
				 28.32    0.000049           6         8           mmap
				 17.34    0.000030           8         4           mprotect
				 11.56    0.000020          20         1           munmap
				 10.40    0.000018           6         3         3 access
				 9.83    0.000017           9         2           open
				 5.78    0.000010           3         3           fstat
				 5.20    0.000009           9         1           write
				 4.05    0.000007           7         1           execve
				 2.31    0.000004           4         1           read
				 2.31    0.000004           2         2           close
				 1.73    0.000003           3         1           brk
				 1.16    0.000002           2         1           arch_prctl
				 ------ ----------- ----------- --------- --------- ----------------
				 100.00    0.000173                    28         3 total
			包括使用了那些系统调用，调用次数，消耗时间等等信息

			
		系统调用的具体执行过程 ：
			用户程序调用C库API（C库中封装有 INT 0x80 软中断指令）
			若该C库API需要进行系统调用，则会使用INT 0x80软中断指令
			INT 0x80 这条指令的执行会让系统跳转到一个预设的内核空间地址，即system_call函数
			system_call 根据具体的系统调用号，查找系统调用表，转到执行具体的系统调用服务例程
			CPU执行该系统服务例程
			当系统调用完成后，把控制权交回到发起调用的用户进程前


 ```
  + 采分点：说明了strace的大致用途，说明了系统调用的具体执行过程（包括应用，CPU硬件，操作系统的执行过程）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```
 
## 3.5 ucore系统调用分析
 1. ucore的系统调用中参数传递代码分析。
 	以系统调用read为例：
		用户态:
			read(fd, base, len) ==> sys_read(fd, base, len)
					 	   		==> syscall(int num, ...)
								==> 内核态 trap(struct trapframe *tf)
		内核态:
			trap(trapframe) ==> trap_dispatch(trapframe)
							==> syscall()  (case T_SYSCALL)
							==> syscalls[num](arg) : sys_read(uint32_t arg[])
							==> sysfile_read(fd, base, len)
    
			
 2. ucore的系统调用中返回结果的传递代码分析。
 3. 以ucore lab8的answer为例，分析ucore 应用的系统调用编写和含义。
 4. 以ucore lab8的answer为例，尝试修改并运行代码，分析ucore应用的系统调用执行过程。
 
## 3.6 请分析函数调用和系统调用的区别
 1. 请从代码编写和执行过程来说明。
   i. 说明`int`、`iret`、`call`和`ret`的指令准确功能
 
