

### DÉPLOIEMENT 
1. Construction : ```docker build -t tls1 .```
2. Lancement : ```docker run -d -p 443:443 --name tls1 tls1```


### CONFIGURATION FIREFOX (about:config) ---
* ```security.tls.version.min = 1```
  (Permet de descendre jusqu'au protocole 1.0 )
* ```security.tls.version.enable-deprecated = true```
  (Désactive l'écran d'avertissement bloquant les versions obsolètes)


### ANALYSE WIRESHARK ( ce contenu a été généré et pas testé)
* Interface : docker0 (Linux) ou Loopback (Win/Mac)
* Filtre : ```tls.handshake.version == 0x0301```

