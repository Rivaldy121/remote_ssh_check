import paramiko
import logging
import pandas as pd

# Logging error hanya di level critical saja
logging.basicConfig(level=logging.CRITICAL)

# Membuat variabel untuk memantau hasil ping
recieved_status = 8
rtt_detail = 9

# Membuat objek SSHClient
ssh = paramiko.SSHClient()

# Mengambil list IP address dari file
ip_list = pd.read_csv("./data/ip_addresses.csv")

# Validasi kolom pada variabel ip_list
required_columns = ['IP', 'username', 'password', 'port']
if not set(required_columns).issubset(ip_list.columns):
    raise ValueError("Kolom yang diperlukan tidak ada dalam file CSV")

if ip_list['IP'].duplicated().any():
    raise ValueError("Terdapat IP yang sama (duplikat)")

# Eksekusi perintah SSH ke list IP pada variabel ip_list
def open_ssh():
    ssh.connect(hostname=ip_address, port=ip_port, username=user_name, password=pswd)
    print ("Success login to ", ip_address)

# Eksekusi perintah Ping WA
def ping_wa():
    # Menjalankan perintah di server
    stdin, stdout, stderr = ssh.exec_command('ping -c 5 whatsapp.com')

    # Menampilkan hasil dari perintah
    hasil_ping = stdout.readlines()
    print("WhatsApp Ping Result :")
    print(hasil_ping[recieved_status]+hasil_ping[rtt_detail])
    conn = ssh.invoke_shell()

# Eksekusi perintah SSH dan Ping WA untuk setiap baris pada ip_list
for i in range(len(ip_list)):
    ip_address = ip_list.iloc[i, 0]
    user_name = ip_list.iloc[i, 1]
    pswd = ip_list.iloc[i, 2]
    ip_port = int(ip_list.iloc[i, 3])

    # Menambahkan host key untuk server yang belum pernah diakses sebelumnya
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print ("--------------------------------------")
    print ("Trying Connection to ", ip_address)

    # Buka koneksi SSH
    try:
        open_ssh()
    except:
        print(ip_address,"tidak dapat diakses \n")

    # Ping ke whatsapp.com
    try:
        ping_wa()
    except:
        print(ip_address,"gagal PING WA \n")

    # Menutup koneksi
    ssh.close()