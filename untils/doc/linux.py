Linux系统信息
1.查看Linux服务器操作系统的信息
#lsb_release -a      或者  #cat   /etc/issue
2.查看Linux系统运行的内核版本
#cat /proc/version
CPU的信息
1.查看cpu的型号
#cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c
2.查看Linux系统物理cpu个数----硬件实际个数
#cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
3.查看Linux系统逻辑cpu个数
#cat /proc/cpuinfo |grep "processor"|sort -u|wc -l
内存信息
1.查看Linux系统的总内存及使用情况
#free  -m       或者  #top -M     或者  #cat  /proc/meminfo | grep MemTotal
硬盘信息
1 .查看硬盘及分区情况
#lsblk       或者  #fdisk  -l      
2.查看硬盘大小及使用情况
#df  -h     
注：使用 #df -HT，查看出来的硬盘大小是以1G=1000M计算得出
网卡信息
1.查看网卡的硬件信息
#lspci | grep -i 'eth'
2.查看网卡的网络接口
 #ifconfig -a
查看系统登录日志
日志文件 /var/log/wtmp ，系统的每一次登录，都会在此日志中添加记录，为了防止有人篡改，该文件为二进制文件 （可查看登录的ip信息
#cd   /var/log ; last  或者  last -f /var/log/wtmp 
查看并清除僵尸进程
#ps -e -o ppid,stat | grep Z | cut -d" " -f2 | xargs kill -9
#kill -HUP `ps -A -ostat,ppid | grep -e '^[Zz]' | awk '{print $2}'`
使用kill批量终止进程
#ps -ef | grep 进程名 | grep -v grep | awk '{print $2}' | xargs kill -9

