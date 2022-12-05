import os
import subprocess
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

#获取本机网卡名称和ipv4
def get_yitainame_and_ipv4():
    p =subprocess.Popen("ipconfig",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding="gb2312")
    d =  p.communicate()[0]
    date = d[d.find("以太网适配器"):]
    while True:
        a = date.find("媒体状态") - date.find("以太网适配器")
        if 0< a < 20:
            date = date[date.find("连接特定") + 28:]
        else:
            break
    return date[date.find("以太网适配器")+6:date.find(":")].strip(),date[date.find("IPv4 地址"):-1].split()[15]

#设置ipv6
def set_ipv6(wangka_name,ip,wangguan):
    cmd_set_ip =f"netsh interface ipv6 set address \"{wangka_name}\" {ip}"
    cmd_set_wangguan = f"netsh interface ipv6 add route ::/0 \"{wangka_name}\"  {wangguan}"
    a = subprocess.run(cmd_set_ip)
    b = subprocess.run(cmd_set_wangguan)
    return a,b

#自动ping网关
def cmd_ping_ipv6(wangguan):
    a =subprocess.run("ping  "+wangguan,shell=True, stdout=None, stderr=None,encoding="gb2312")
    return a

if __name__ == '__main__':
    yitainame,ip =  get_yitainame_and_ipv4()
    print(f"你的网卡名字:{yitainame}")
    print(f"你的ipv4地址:{ip}")
    l = get_ipv6_Gateway(ip)
    if l == False :
        print("你所在的网段不能自动配置IP,请联系开发者")
        os.system("pause")
    else:
        a,b=set_ipv6(yitainame, l[0], l[1])
        if a.returncode == 0:
            print("设置ipv6成功")
            print("你的ipv6地址为:"+l[0])
            print("你的ipv6网关为:"+l[1])
            print("正在ping网关中,请勿退出程序")
            a = cmd_ping_ipv6(l[1])
            if a.returncode ==0:
                print("ping网关成功")
                os.system("pause")
            else:
                print("ping网关失败")
                os.system("pause")
        else:
            print("请右键以管理员身份运行脚本")
            os.system("pause")
