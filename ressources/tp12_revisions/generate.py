#!/usr/bin/env python3
"""
Génère les artefacts du TP12 (révisions) : scan.txt, capture.pcap,
note_attaquant.txt, archive.enc — puis les empaquette dans enquete.zip.

Scénario : PME belge compromise.
  - Victime  : 192.168.1.10  (MAC 00:0c:29:11:22:10)
  - Passerelle : 192.168.1.1 (MAC légitime 00:0c:29:00:00:01)
  - Attaquant : 192.168.1.50 (MAC 00:0c:29:aa:bb:50)
  - Mot de passe intercepté : Brussels1830
  - Flag : FLAG{ARP_spoofing_detected}
"""

import os
import base64
import hashlib
import subprocess
import zipfile
from pathlib import Path

from scapy.all import Ether, ARP, IP, TCP, Raw, wrpcap

HERE = Path(__file__).parent
OUT = HERE / "build"
OUT.mkdir(exist_ok=True)

PASSWORD = "Brussels1830"
FLAG = "FLAG{ARP_spoofing_detected}"

ATTACKER_MAC = "00:0c:29:aa:bb:50"
ATTACKER_IP = "192.168.1.50"
VICTIM_MAC = "00:0c:29:11:22:10"
VICTIM_IP = "192.168.1.10"
GATEWAY_IP = "192.168.1.1"
WEB_SERVER_IP = "10.20.30.40"


# ----------------------------------------------------------------------
# 1. scan.txt — faux rapport nmap (Metasploitable-like)
# ----------------------------------------------------------------------
SCAN_TXT = """Starting Nmap 7.80 ( https://nmap.org ) at 2026-05-18 03:14 CEST
Nmap scan report for portail-pme.lan (192.168.1.10)
Host is up (0.00021s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
MAC Address: 00:0C:29:11:22:10 (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.23 seconds
"""

(OUT / "scan.txt").write_text(SCAN_TXT)
print(f"[+] scan.txt          ({len(SCAN_TXT)} octets)")


# ----------------------------------------------------------------------
# 2. note_attaquant.txt — message base64
# ----------------------------------------------------------------------
NOTE_CLAIR = (
    "Salut Loïc,\n"
    "J'ai chiffre l'archive avec AES-256-CBC (PBKDF2).\n"
    "La cle = MD5(mot de passe admin intercepte sur le portail), en hex minuscules.\n"
    "Decoupe pas le MD5, prends les 32 caracteres bruts.\n"
    "Je file. Efface ce fichier apres lecture.\n"
)
note_b64 = base64.b64encode(NOTE_CLAIR.encode("utf-8")).decode("ascii")
# On ajoute un saut de ligne final pour que `cat` rende lisiblement
(OUT / "note_attaquant.txt").write_text(note_b64 + "\n")
print(f"[+] note_attaquant.txt ({len(note_b64)} chars b64)")


# ----------------------------------------------------------------------
# 3. archive.enc — AES-256-CBC PBKDF2 avec clé = MD5(PASSWORD)
# ----------------------------------------------------------------------
md5_key = hashlib.md5(PASSWORD.encode("utf-8")).hexdigest()
print(f"    MD5(\"{PASSWORD}\") = {md5_key}")

flag_path = OUT / "flag.txt"
flag_path.write_text(FLAG + "\n")

archive_path = OUT / "archive.enc"
# Utilise openssl en sous-processus pour garantir la compatibilité bit-à-bit
# avec ce que les étudiants utiliseront pour déchiffrer.
subprocess.run(
    [
        "openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt",
        "-in", str(flag_path),
        "-out", str(archive_path),
        "-k", md5_key,
    ],
    check=True,
)
print(f"[+] archive.enc       ({archive_path.stat().st_size} octets)")


# ----------------------------------------------------------------------
# 4. capture.pcap — 3 paquets (2 ARP + 1 HTTP)
# ----------------------------------------------------------------------
# Packet 1 : ARP request légitime de l'attaquant ("who has 192.168.1.10?")
#   → établit pour l'analyste que MAC 00:0c:29:aa:bb:50 correspond à .50
pkt1 = Ether(src=ATTACKER_MAC, dst="ff:ff:ff:ff:ff:ff") / \
       ARP(op=1,
           hwsrc=ATTACKER_MAC, psrc=ATTACKER_IP,
           hwdst="00:00:00:00:00:00", pdst=VICTIM_IP)
pkt1.time = 1747555200.000000

# Packet 2 : ARP reply spoofé — même MAC, mais cette fois prétend être .1
#   → c'est la spoofing : MAC de l'attaquant ↔ IP de la passerelle
pkt2 = Ether(src=ATTACKER_MAC, dst=VICTIM_MAC) / \
       ARP(op=2,
           hwsrc=ATTACKER_MAC, psrc=GATEWAY_IP,
           hwdst=VICTIM_MAC, pdst=VICTIM_IP)
pkt2.time = 1747555200.523412

# Packet 3 : HTTP GET de la victime
#   → eth.dst = ATTACKER_MAC (cache empoisonné !)
#   → ip.dst  = WEB_SERVER_IP (la victime croit parler au vrai serveur)
http_payload = (
    b"GET /admin/ HTTP/1.1\r\n"
    b"Host: portail-pme.lan\r\n"
    b"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0\r\n"
    b"Accept: text/html,application/xhtml+xml\r\n"
    b"Accept-Language: fr-BE,fr;q=0.8\r\n"
    b"Authorization: Basic " + base64.b64encode(
        f"admin:{PASSWORD}".encode("ascii")
    ) + b"\r\n"
    b"Connection: keep-alive\r\n"
    b"\r\n"
)
pkt3 = Ether(src=VICTIM_MAC, dst=ATTACKER_MAC) / \
       IP(src=VICTIM_IP, dst=WEB_SERVER_IP, id=0x1234, ttl=64) / \
       TCP(sport=51234, dport=80, flags="PA", seq=1000, ack=2000, window=64240) / \
       Raw(load=http_payload)
pkt3.time = 1747555202.847291

pcap_path = OUT / "capture.pcap"
wrpcap(str(pcap_path), [pkt1, pkt2, pkt3])
print(f"[+] capture.pcap      ({pcap_path.stat().st_size} octets)")


# ----------------------------------------------------------------------
# 5. enquete.zip
# ----------------------------------------------------------------------
zip_path = HERE / "enquete.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for name in ("scan.txt", "capture.pcap", "note_attaquant.txt", "archive.enc"):
        zf.write(OUT / name, arcname=f"enquete/{name}")

print(f"\n[✓] {zip_path.name} prêt ({zip_path.stat().st_size} octets)")
print(f"    Mot de passe : {PASSWORD}")
print(f"    MD5 (clé)    : {md5_key}")
print(f"    Flag         : {FLAG}")
