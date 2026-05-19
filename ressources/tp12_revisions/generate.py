#!/usr/bin/env python3
"""
Régénère les artefacts dérivés du TP12 (révisions) :
- scan.txt
- note_attaquant.txt
- archive.enc
- enquete.zip (qui inclut aussi les deux pcap capture_1/capture_2 livrés par le prof)

Les pcap (capture_1.pcap = ARP spoofing, capture_2.pcap = HTTP Basic) sont
fournis manuellement dans build/ et NE sont PAS générés par ce script.

Indépendance des exercices :
  - §2 (pcap) → l'étudiant intercepte 'user:bubblegum' dans capture_2.pcap
  - §4-5 (archive) → l'étudiant utilise le mdp donné dans la note (EPHEC2026)
  Les deux mots de passe sont DIFFÉRENTS → les exercices sont indépendants.
"""

import base64
import hashlib
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "build"
OUT.mkdir(exist_ok=True)

# Mot de passe servant à dériver la clé de chiffrement de archive.enc.
# Distinct du mot de passe intercepté dans capture_2.pcap (qui est 'bubblegum').
ARCHIVE_PASSWORD = "EPHEC2026"
FLAG = "FLAG{ARP_spoofing_detected}"


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
# 2. note_attaquant.txt — message base64 mentionnant directement le mdp
#    (pour que les exos soient indépendants du pcap)
# ----------------------------------------------------------------------
NOTE_CLAIR = (
    "Salut Loic,\n"
    "J'ai chiffre l'archive avec AES-256-CBC (PBKDF2).\n"
    f"La cle est MD5('{ARCHIVE_PASSWORD}') en hex minuscules.\n"
    "Decoupe pas le MD5, prends les 32 caracteres bruts.\n"
    "Je file. Efface ce fichier apres lecture.\n"
)
note_b64 = base64.b64encode(NOTE_CLAIR.encode("utf-8")).decode("ascii")
(OUT / "note_attaquant.txt").write_text(note_b64 + "\n")
print(f"[+] note_attaquant.txt ({len(note_b64)} chars b64)")


# ----------------------------------------------------------------------
# 3. archive.enc — AES-256-CBC PBKDF2 avec clé = MD5(ARCHIVE_PASSWORD)
# ----------------------------------------------------------------------
md5_key = hashlib.md5(ARCHIVE_PASSWORD.encode("utf-8")).hexdigest()
print(f"    MD5(\"{ARCHIVE_PASSWORD}\") = {md5_key}")

flag_path = OUT / "flag.txt"
flag_path.write_text(FLAG + "\n")

archive_path = OUT / "archive.enc"
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
# 4. enquete.zip — empaquette tout (les deux pcap doivent déjà être dans build/)
# ----------------------------------------------------------------------
required = ("scan.txt", "capture_1.pcap", "capture_2.pcap",
            "note_attaquant.txt", "archive.enc")
missing = [n for n in required if not (OUT / n).exists()]
if missing:
    raise SystemExit(
        f"❌ Fichiers manquants dans build/ : {missing}\n"
        f"   capture_1.pcap et capture_2.pcap doivent être fournis manuellement."
    )

zip_path = HERE / "enquete.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for name in required:
        zf.write(OUT / name, arcname=f"enquete/{name}")

print(f"\n[✓] {zip_path.name} prêt ({zip_path.stat().st_size} octets)")
print(f"    Mdp archive   : {ARCHIVE_PASSWORD}")
print(f"    MD5 (clé)     : {md5_key}")
print(f"    Mdp dans pcap : user:bubblegum (capture_2.pcap)")
print(f"    Flag          : {FLAG}")
