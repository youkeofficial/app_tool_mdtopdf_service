# Déploiement du Convertisseur Markdown vers PDF (md-to-pdf)

Ce projet est à présent **prêt pour la production (Production-Ready)**. 
Voici ce qui a été analysé, configuré et comment déployer cette application robuste.

## 1. Modifications apportées pour la production
Dans le fichier `backend/Dockerfile`, je me suis assuré que le projet n'utilise plus le serveur de développement basique de Flask (`app.run()`). 
La commande utilise désormais **Waitress**, un serveur WSGI Python robuste parfaitement optimisé pour la production. 
La commande a été remplacée par `CMD ["waitress-serve", "--port=5001", "app:app"]`. Waitress était déjà disponible dans vos dépendances.

## 2. Architecture des ports
Votre fichier `docker-compose.yml` orchestre deux conteneurs :
- **`mdtopdf-service` (Port 5001)** : Le cœur de l'application Flask/Waitress responsable réellement de la génération des PDF.
- **`mdtopdf-mcp` (Port 8001)** : Le serveur Agentic FastMCP (Model Context Protocol). Il sert d'interface SSE pour permettre à des agents IA ou vos autres SaaS de générer des PDF via des appels standardisés.

Le volume local `./backend/pdfs` est monté sur `/app/pdfs` (dans les deux conteneurs) pour assurer la persistance de vos documents même si les conteneurs redémarrent.

## 3. Comment construire (build) l'image Docker [Optionnel]
Si vous souhaitez d'abord builder l'image manuellement (ex. pour la pousser sur Docker Hub) :

```bash
cd c:\prog\apps\md-to-pdf

# Construire l'image manuellement
docker build -t inspirify-mdtopdf:latest ./backend
```
*Note : Docker Compose s'en chargera automatiquement grâce au chemin de build (`./backend`) spécifié.*

## 4. Comment déployer sur n'importe quel serveur (VPS, Portainer, etc.)

**Via Docker Compose en ligne de commande :**
Idéal pour un VPS standard (Ubuntu, Debian, etc.).
1. Copiez les fichiers/dossiers du projet sur votre serveur de production.
2. Déplacez-vous à la racine de votre application (`cd /chemin/vers/md-to-pdf`).
3. Lancez la flotte d'applications :
   ```bash
   docker-compose up --build -d
   ```

**Via Portainer (Interface WEB) :**
Si vous gérez le VPS via Portainer, c'est encore plus simple :
1. Accédez au menu "Stacks" puis "Add stack".
2. Copiez-collez tout votre fichier `docker-compose.yml` (ou liez-le à un repo GitHub privé).
3. Cliquez sur "Deploy the stack". Portainer s'occupera de tout créer, builder et lancer.

## 5. Comment vérifier que tout marche bien ?
Une fois déployé :
- Service HTTP : Naviguez sur `http://VOTRE_IP_SERVEUR:5001` (où l'API REST `POST /api/v1/convert` vous attend).
- Service MCP : Tourne proprement sous SSE sur `http://VOTRE_IP_SERVEUR:8001` pour vos IA.

Les documents générés s'empileront en toute sécurité dans votre dossier `backend/pdfs`.
