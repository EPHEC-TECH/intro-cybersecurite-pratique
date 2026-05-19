---
nav_exclude: true
---

# TP12 — Artefacts d'examen

Contenu de `enquete.zip` (à distribuer aux étudiants) :

| Fichier | Description |
|---|---|
| `scan.txt` | Faux rapport nmap (services Metasploitable-like) |
| `capture_1.pcap` | Trafic ARP spoofing (fournis manuellement, non régénéré par `generate.py`) |
| `capture_2.pcap` | Trafic HTTP avec Authorization Basic — mdp `user:bubblegum` |
| `note_attaquant.txt` | Message base64 indiquant le mdp à hasher (différent du pcap !) |
| `archive.enc` | AES-256-CBC PBKDF2, clé = MD5(mdp indiqué dans la note) |

## Indépendance pédagogique

Les exercices §2 (analyse pcap) et §4-5 (déchiffrement) utilisent **des mots de passe différents**. Les deux peuvent être résolus indépendamment l'un de l'autre.

## Régénération

```bash
pip install scapy
python3 generate.py
```

⚠️ Le script attend que `build/capture_1.pcap` et `build/capture_2.pcap` existent
(ces deux pcaps sont fournis manuellement et **ne sont pas** régénérés).
Si tu changes l'un des pcaps, recopie-le dans `build/` avant de lancer le script.

## Valeurs sensibles

- **Mot de passe intercepté (dans capture_2.pcap)** : `bubblegum`
- **Mot de passe de l'archive (donné dans la note)** : `EPHEC2026`
- **Hash MD5 de la clé** : `790c5ca00b309cfb9910587f1981e033`
- **Flag** : `FLAG{ARP_spoofing_detected}`

⚠️ Pour changer le mdp de l'archive : éditer `generate.py` (variable `ARCHIVE_PASSWORD`)
puis relancer le script.
