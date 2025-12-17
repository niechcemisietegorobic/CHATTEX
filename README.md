# CHATTEX – CHATTUJ DO WOLI 💬

CHATTEX to webowa aplikacja typu **czat + forum**, stworzona jako projekt zespołowy
z zakresu **chmur obliczeniowych / aplikacji webowych**.

Aplikacja umożliwia:
- publiczny czat wszystkich użytkowników,
- prywatne wiadomości (DM),
- publikowanie postów na forum,
- nowoczesny, wyśrodkowany interfejs z tłem graficznym.

---

## 🧩 Funkcjonalności

### 👥 Użytkownicy
- rejestracja i logowanie użytkowników,
- uwierzytelnianie za pomocą tokenów JWT.

### 💬 Publiczny czat
- wspólny kanał dla wszystkich zalogowanych użytkowników,
- automatyczne odświeżanie wiadomości.

### 🔒 Prywatne wiadomości
- wybór użytkownika z listy,
- dwukierunkowa komunikacja prywatna.

### 🧵 Forum
- tworzenie postów (tytuł + treść),
- lista postów widoczna dla wszystkich użytkowników.

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

## 🚀 Uruchomienie aplikacji (lokalnie)

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

## 👨‍💻 Autor
Projekt wykonany zespołowo (podział na 3 części).

Autor części aplikacyjnej:
NASZE INDEXY

---

## 📸 Zrzuty ekranu
Zrzuty ekranu znajdują się w katalogu:
```
screenshots/
```
=======
# project-app
projekcik
>>>>>>> 04ac0d261072f10c79f67a9a6379b57e6ab19b61
