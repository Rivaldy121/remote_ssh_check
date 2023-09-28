import paramiko
import logging
import pandas as pd

logging.basicConfig(level=logging.CRITICAL)

# Membuat objek SSHClient
ssh = paramiko.SSHClient()

# Mengambil list IP address dari file
ip_list = pd.read_csv("./data/ip_addresses.csv")

def excute():
    ssh.connect(hostname=ip_address, port=ip_port, username=user_name, password=pswd)
    print ("Success login to ", ip_address)

    # Ping ke whatsapp.com
    try:
        ping_wa()
    except:
        print(ip_address,"gagal PING WA \n")

    # Menutup koneksi
    ssh.close()

def ping_wa():
    # Menjalankan perintah di server
    stdin, stdout, stderr = ssh.exec_command('ping -c 5 whatsapp.com')

    # Menampilkan hasil dari perintah
    hasil_ping = stdout.readlines()
    print("WhatsApp Ping Result :")
    print(hasil_ping[8]+hasil_ping[9])
    conn = ssh.invoke_shell()

# Menambahkan host key untuk server yang belum pernah diakses sebelumnya
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(len(ip_list)):
    ip_address = ip_list.iloc[i, 0]
    user_name = ip_list.iloc[i, 1]
    pswd = ip_list.iloc[i, 2]
    ip_port = int(ip_list.iloc[i, 3])

    print ("Trying Connection to", ip_address)

    try:
        # Koneksi ke server
        excute()
    except:
        print(ip_address,"tidak dapat diakses \n")