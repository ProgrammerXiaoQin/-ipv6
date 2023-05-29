#!/usr/bin/python3.8
#encoding:utf-8
import os
import re
import subprocess
#不同ip段对应的ipv6前缀
ip_dict = {
    "10.154.82":"2409:808E:4950:206::",
    "10.154.83":"2409:808E:4950:207::",
    "10.154.87":"2409:808E:4950:200::",
    "10.154.88":"2409:808E:4950:201::",
    "10.154.85":"2409:808E:4950:203::",
    "10.154.93":"2409:808E:4950:1202::",
    "10.154.94":"2409:808E:4950:1208::",
    "10.154.95":"2409:808E:4950:1206::",
}

#通过ip获取ipv6地址和网关
def get_ipv6_Gateway(ipv4):
    ip = ipv4[:9]
    ipend = hex(int(ipv4[10:]))[2:].upper()
    if ip in ip_dict.keys():
        return ip_dict[ip]+ipend,ip_dict[ip]+"1"
    else:
        return False

#获取本机网卡名和ipv4
def get_yitainame_and_ipv4():
    # 执行ip addr命令,用communicate()方法获取执行结果信息，第[0],命令输出结果
    p = subprocess.Popen("ip addr", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         encoding="utf-8").communicate()[0]
    # 正则匹配网卡名
    wangka_name = re.findall("2: ([\w\d]{1,8}):", p)[0]
    # 正则匹配对应ip
    ipv4 = re.findall('10.154.[\d]{2,3}.[\d]{2,3}', p)[0]
    return wangka_name, ipv4

#获取对应网卡名的uuid
def get_uuid(wangka_name):
    # 查看所有网络连接
    p = subprocess.Popen("nmcli connection show",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="utf-8").communicate()[0]
    # 正则匹配对应网卡的uuid
    uuid = re.findall(f'.*{wangka_name}',p)[0].split()[-3]
    return uuid

# 设置ipv6
def set_ipv6(uuid,ip,wangguan):
    # cmd_set_ip =f"netsh interface ipv6 set address \"{wangka_name}\" {ip}"
    # cmd_set_wangguan = f"netsh interface ipv6 add route ::/0 \"{wangka_name}\"  {wangguan}"
    a = subprocess.run(f"nmcli con mod '{uuid}' ipv6.addresses {ip}/64 ipv6.gateway {wangguan}  ipv6.method manual",shell=True)

    return a.returncode

# 自动ping网关
def cmd_ping_ipv6(wangguan):
    a = subprocess.run("ping6  -c 4 "+wangguan,shell=True, stdout=None, stderr=None,encoding="utf-8")
    return a

if __name__ == '__main__':
    yitainame,ip =  get_yitainame_and_ipv4()
    print(f"网卡:{yitainame}")
    print(f"ipv4:{ip}")
    l = get_ipv6_Gateway(ip)
    uuid = get_uuid(yitainame)
    print(l)
    if l == False :
        print("你所在的网段不能自动配置IP,请联系开发者")
        os.system("pause")
    else:
        a=set_ipv6(uuid, l[0], l[1])
        if a == 0:
            print("设置ipv6成功")
            print("你的ipv6地址为:"+l[0])
            print("你的ipv6网关为:"+l[1])
            print("正在ping网关中,请勿退出程序")
            a = cmd_ping_ipv6(l[1])
            if a.returncode ==0:
                print("ping网关成功")
            else:
                print("ping网关失败")
        else:
            print("请以管理员身份运行脚本")
