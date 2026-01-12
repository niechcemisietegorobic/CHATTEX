# CHATTEX – CHATTUJ DO WOLI 💬

![](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiQVR2cklYaGRwRkZVK1EyQ1NKQm1FdkgzY3lFOThLT0toRkpMQTZMa2taM0ppVHVJODZ3M243UlI5RE8yVkZkMFpMSDhFYUU1OXFDb1l1WGNSRmN1cEVJPSIsIml2UGFyYW1ldGVyU3BlYyI6Ikd5cWlQeE8xdHBMTGFkRUsiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

![](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZ1lCdzVqV3JJT1FhWld6K0I4QzYwdG84bUcxQ01GbVpFRjc4QTNzSmJrbUJoOHZ1Z0szV1pXVHZ6dVZCSVB5Zlk5aHY0R1lad09TbWFha0FUVGYxblpnPSIsIml2UGFyYW1ldGVyU3BlYyI6InhvUk1VOWFMZUpBaFZEMkQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

CHATTEX to webowa aplikacja typu **czat + forum**, stworzona jako projekt zespołowy
z zakresu **chmur obliczeniowych / aplikacji webowych**.

Aplikacja umożliwia:
- publiczny czat wszystkich użytkowników,
- prywatne wiadomości (DM),
- publikowanie postów na forum,
- nowoczesny, wyśrodkowany interfejs z tłem graficznym.

---

## 🏗 Architektura aplikacji

Aplikacja składa się z dwóch głównych komponentów:

### Backend
- Python + Flask
- REST API
- JWT (autoryzacja)

Katalog:
```
backend/
```

### Frontend
- VUE js 
- komunikacja z backendem przez REST API

Katalog:
```
frontend/
```

---

## Uruchomienie aplikacji (lokalnie)

### Backend
```bash
cd backend
source venv/bin/activate
export SECRET_KEY="dev_secret_key_123"
python3 app.py
```

Backend działa na:
```
http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
export VITE_CHATTEX_API_URL="http://localhost:5000"
export VITE_CHATTEX_WEBSOCKET_API_URL="ws://localhost:5000"
npm run dev
```

Frontend dostępny pod:
```
http://localhost:5173
```

---

## ☁️ Docelowa architektura chmurowa (AWS)

Projekt jest przygotowany pod wdrożenie w chmurze AWS:
- Application Load Balancer (public subnet),
- EC2 (Auto Scaling Group, private subnet),
- RDS (relacyjna baza danych, private subnet),
- VPC z podziałem na public/private subnety,
- kod aplikacji pobierany z GitHub.
- frontend budowany przez aws code build i umieszczany na publicznym S3
---

## 👨‍💻 Autorzy
Projekt wykonany zespołowo (podział na 3 części).

NASZE INDEXY

---
