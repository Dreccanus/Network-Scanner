import os
import subprocess
import shutil
import nmap


def ports():
    term_width, _ = shutil.get_terminal_size()
    middle_pos = term_width // 2 - len("looking for open ports ...") // 2
    print(" " * middle_pos, end="")
    print('\033[1;32mAnalysing ....\033[0m')
    commands = ['ss -antp']
    
    command1 = ('cat /etc/hostname /etc/hosts /etc/resolv.conf 2>/dev/null | grep -v "^#" && echo "  \nInterfaces\n" && cat /etc/networks 2>/dev/null && echo "\n" && (ifconfig || ip a) 2>/dev/null')
    
    command2 = ('netstat -rn 2>/dev/null && echo "\n" && (timeout 1 iptables -L 2>/dev/null && cat /etc/iptables/* | grep -v "^#" | grep -Ev "\W+\#|^#" 2>/dev/null) 2>/dev/null  && lsof -i')

    command3 = ('nmcli device show')
    command4 = ['hostname', '-I']

    p = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    output = stdout.decode()
    
    x = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutx, stderr = x.communicate()
    outpux = stdoutx.decode()

    c = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutc, stderr = c.communicate()
    outpuc = stdoutc.decode()
    d = subprocess.Popen(command3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutd, stderr = d.communicate()
    outpud = stdoutd.decode()
    
    
    

    print('\033[1;31m' + output + '\033[0m')
    print('\033[1;32m' + outpux + '\033[0m')
    print('\033[1;31m' + outpuc + '\033[0m')
    print('\033[1;32m' + outpud + '\033[0m')
    


    k = subprocess.run(command4, capture_output=True, text=True)
    ip_address = k.stdout.strip()

    octets = ip_address.split('.')
    octets[-1] = '0/24'
    new_ip = '.'.join(octets)





    nm = nmap.PortScanner()
    nm.scan(hosts=new_ip, arguments='-sP -n -e eth0')
    term_width, _ = shutil.get_terminal_size()
    middle_pos = term_width // 2 - len("Discover All The IP Addresses") // 2
    print(" " * middle_pos, end="")
    print('\033[1;31mDiscover All The IP Addresses\033[0m')

    
# Create a new instance of the PortScanner class
    scanner = nmap.PortScanner()

# Use the scan method to perform a ping sweep of the network
    scanner.scan(hosts=new_ip, arguments="-sn")

# Get a list of all the live hosts in the network
    hosts = [host for host in scanner.all_hosts() if scanner[host]["status"]["state"] == "up"]

# Loop over each live host and scan it for open ports
    try:
        for host in hosts:
            scanner.scan(hosts=host, arguments="-p 1-65535")
            print(f"\033[1;33mIP Address: {host}\033[0m")
            print(f"\033[1;33mOpen Ports: {list(scanner[host]['tcp'].keys())}\n\033[0m")

    except KeyError:

        print ("no port found !")
        command8 = ("sudo tcpdump -i eth0 -w ouii -G 5")
    rrrc = input ("\033[1;34mWould you like to sniff into your Network for 20 sec? (Yes/No): \033[0m")
    if rrrc.lower() == "yes":
        

        command8 = ['sudo', 'tcpdump', '-i', 'eth0', '-w', 'capture.pcap', '-G', '10', '-W', '1']
        tcpdumpceo = subprocess.Popen(command8, stdout=subprocess.PIPE)
        tcpdumpceo.wait()
        command9 = ['sudo', 'tcpdump', '-r', 'capture.pcap']
        tcpdumpce1 = subprocess.Popen(command9, stdout=subprocess.PIPE)
        lessceo = subprocess.Popen(['less', '-R'], stdin=tcpdumpce1.stdout)
        lessceo.wait()
        print("\033[1;34mFinished viewing packets\033[0m")


        print("\033[1;34mPacket capture complete.\033[0m")
    elif rrrc.lower() == "no":
        print ("Okay, have fun!")
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")

def main():
    ports()

if __name__ == "__main__":
    main()
