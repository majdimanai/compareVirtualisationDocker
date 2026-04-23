Projet réalisé par Manai Majdi , Mahroug Rayen et Riadh Chelbi
# 🐳 SentimentIA — Docker vs VM

Analyse de sentiment avec comparaison Docker ↔ VM en temps réel.

---

## 📁 Structure du projet

```
sentiment-app/
├── backend/
│   ├── app.py              # API FastAPI
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker
├── frontend/
│   └── index.html          # Interface web
├── docker-compose.yml      # Orchestration Docker + VM simulée
└── README.md
```

---

## 🚀 Déploiement rapide (Docker + VM simulée)

### Prérequis
- Docker Desktop installé et lancé
- Python 3.9+

### Étape 1 — Lancer Docker

```bash
cd sentiment-app
docker-compose up --build -d
```

Cela lance :
- 🐳 **Docker** sur `http://localhost:8000`
- 🖥 **VM simulée** sur `http://localhost:8001`

### Étape 2 — Vérifier que ça tourne

```bash
curl http://localhost:8000/health
# → {"status":"healthy","env":"docker"}

curl http://localhost:8001/health
# → {"status":"healthy","env":"vm"}
```

### Étape 3 — Ouvrir le frontend

Ouvrir `frontend/index.html` dans ton navigateur.
Les URLs sont pré-configurées : `localhost:8000` et `localhost:8001`.

---

## 🖥 Déploiement sur une vraie VM (optionnel)

Si tu as une vraie VM Ubuntu/Debian :

```bash
# Sur la VM — installer Python
sudo apt update && sudo apt install python3 python3-pip -y

# Copier les fichiers backend sur la VM
scp -r backend/ user@IP_DE_LA_VM:/home/user/sentiment-backend/

# Sur la VM — installer les dépendances
cd /home/user/sentiment-backend
pip3 install -r requirements.txt

# Lancer le serveur sur la VM (port 8001)
ENV_TYPE=vm ENV_NAME="VM Ubuntu" uvicorn app:app --host 0.0.0.0 --port 8001
```

Puis dans `index.html`, changer l'URL VM :
- De : `http://localhost:8001`
- À  : `http://IP_DE_LA_VM:8001`

---

## 🧪 Test API manuel

```bash
# Analyser un texte
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker is absolutely amazing!"}'

# Réponse :
{
  "sentiment": "POSITIF",
  "emoji": "😊",
  "score": 0.6369,
  "details": {"positif": 0.405, "négatif": 0.0, "neutre": 0.595},
  "latency_ms": 0.45,
  "env": "docker",
  "env_name": "Docker Container",
  "hostname": "a1b2c3d4e5f6",
  "words": 4
}
```

---

## 🛑 Arrêter les containers

```bash
docker-compose down
```

---

## 🔌 Endpoints API

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Info de l'environnement |
| GET | `/health` | Vérification de santé |
| POST | `/analyze` | Analyse un texte |
# compareVirtualisationDocker
