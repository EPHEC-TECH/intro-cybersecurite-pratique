---
nav_exclude: true
---

# TP12 — Artefacts d'examen

Contenu de `enquete.zip` (à distribuer aux étudiants) :

| Fichier | Description |
|---|---|
| `scan.txt` | Faux rapport nmap (services Metasploitable-like) |
| `capture.pcap` | 3 paquets : 2 ARP spoof + 1 HTTP GET avec Authorization Basic |
| `note_attaquant.txt` | Message base64 indiquant la dérivation de la clé |
| `archive.enc` | AES-256-CBC PBKDF2, clé = MD5(mot de passe intercepté) |

## Régénération

```bash
pip install scapy
python3 generate.py
```

Les artefacts intermédiaires sont placés dans `build/` (gitignoré).
Le `enquete.zip` final est versionné à la racine de ce dossier.

## Valeurs sensibles

- **Mot de passe intercepté** : `Brussels1830`
- **Hash MD5 (clé)** : `39d225445afa619d3b73123141a0f17f`
- **Flag** : `FLAG{ARP_spoofing_detected}`

⚠️ Pour changer ces valeurs : éditer `generate.py` (variables `PASSWORD` et `FLAG`)
puis relancer le script.
