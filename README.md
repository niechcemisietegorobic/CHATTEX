# CHATTEX – CHATTUJ DO WOLI 💬

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
- SQLite (środowisko developerskie)

Katalog:
```
backend/
```

### Frontend
- HTML, CSS, JavaScript (Vanilla JS)
- komunikacja z backendem przez REST API
- statyczny serwer `http.server`

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
python3 -m http.server 8010
```

Frontend dostępny pod:
```
http://localhost:8010
```

---

## ☁️ Docelowa architektura chmurowa (AWS)

Projekt jest przygotowany pod wdrożenie w chmurze AWS:
- Application Load Balancer (public subnet),
- EC2 (Auto Scaling Group, private subnet),
- RDS (relacyjna baza danych, private subnet),
- VPC z podziałem na public/private subnety,
- kod aplikacji pobierany z GitHub.

---

## 👨‍💻 Autorzy
Projekt wykonany zespołowo (podział na 3 części).

NASZE INDEXY

---
