# CHATTEX - CHATTUJ DO WOLI 💬

[![CodeQL Advanced Prod](https://github.com/niechcemisietegorobic/CHATTEX/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/niechcemisietegorobic/CHATTEX/actions/workflows/codeql.yml)
![Frontend Prod Build](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZ1lCdzVqV3JJT1FhWld6K0I4QzYwdG84bUcxQ01GbVpFRjc4QTNzSmJrbUJoOHZ1Z0szV1pXVHZ6dVZCSVB5Zlk5aHY0R1lad09TbWFha0FUVGYxblpnPSIsIml2UGFyYW1ldGVyU3BlYyI6InhvUk1VOWFMZUpBaFZEMkQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

CHATTEX to webowa aplikacja **czat + forum**, stworzona jako projekt zespołowy
z przedmiotu **Bezpieczeństwo serwerów i aplikacji Web** na kierunku Cyberbezpieczeństwo.

Aplikacja umożliwia:
- personalizacje wyglądu
- korzystanie z publicznego czatu
- pisanie prywatnych wiadomości (DM)
- publikowanie i komentowanie postów na forum

---

## Architektura aplikacji

Aplikacja składa się z dwóch głównych komponentów:

### Backend
- Python + Flask, REST API, JWT (autoryzacja)

Katalog:
```
backend/
```

### Frontend
- Vue js, REST API

Katalog:
```
frontend/
```

---

## Uruchamianie aplikacji

W celu poprawnego funkcjonowania aplikacji konieczne jest skonfigurowanie sekretów i zmiennych środowiskowych:

### backend

| Typ  | Nazwa | Opis | 
| ------------- | ------------- | ------------- | 
| Sekret | \<branch\>/chattex/django_secret_key  | sekret używany przez django  |
| Sekret  | \<branch\>/chattex/root_invite  | pierwsze zaproszenie służące do rejestracji na platformie  |
| Zmienna  | IS_DEV  | czy kontener działa w wersji dev  |
| Zmienna  | RDS_URL  | adres bazy PostgreSQL  |
| Zmienna  | CACHE_URL  | adres ElastiCache  |
| Zmienna  | RDS_SM  | nazwa sekretu przechowującego dane logowania RDS  |
| Zmienna  | FRONTEND_URL  | adres origin z którego będą wysyłane requesty API  |
| Zmienna  | MEDIA_BUCKET  | nazwa wiaderka S3 przechowującego media przesłane przez użytkowników  |
| Zmienna  | MEDIA_URL  | adres url z którego udostępniane są media  |
| Zmienna  | REGION  | region w którym uruchomiona jest infrastruktura  |

### frontend

| Typ  | Nazwa | Opis | 
| ------------- | ------------- | ------------- | 
| Parametr  | /CHATTEX_\<branch\>/API_URL  | adres url api https |
| Parametr  | /CHATTEX_\<branch\>/WEBSOCKET_API_URL  | adres url api wss  |

---

## ☁️ Architektura chmurowa (AWS)

### Schemat infrastruktury

![AWS Cloud Architecture Diagram](.github/Chattex_Cloud_Structure.jpg "AWS Cloud Architecture Diagram")

### Schemat CI/CD

![CI/CD pipeline graph](.github/ci_cd.png "CI/CD pipeline graph")

---

