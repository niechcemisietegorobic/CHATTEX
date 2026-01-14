# CHATTEX - CHATTUJ DO WOLI 💬

![Frontend Dev Build](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiQVR2cklYaGRwRkZVK1EyQ1NKQm1FdkgzY3lFOThLT0toRkpMQTZMa2taM0ppVHVJODZ3M243UlI5RE8yVkZkMFpMSDhFYUU1OXFDb1l1WGNSRmN1cEVJPSIsIml2UGFyYW1ldGVyU3BlYyI6Ikd5cWlQeE8xdHBMTGFkRUsiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)
![Frontend Prod Build](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZ1lCdzVqV3JJT1FhWld6K0I4QzYwdG84bUcxQ01GbVpFRjc4QTNzSmJrbUJoOHZ1Z0szV1pXVHZ6dVZCSVB5Zlk5aHY0R1lad09TbWFha0FUVGYxblpnPSIsIml2UGFyYW1ldGVyU3BlYyI6InhvUk1VOWFMZUpBaFZEMkQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

CHATTEX to webowa aplikacja **czat + forum**, stworzona jako projekt zespołowy
z zakresu **chmur obliczeniowych / aplikacji webowych**.

Aplikacja umożliwia:
- zapraszanie nowych użytkowników
- używanie publicznego czatu wszystkich użytkowników
- pisanie prywatnych wiadomości (DM)
- publikowanie i komentowanie postów na forum

---

## 🏗 Architektura aplikacji

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
| Zmienna  | RDS_SECRET  | nazwa sekretu przechowującego dane logowania RDS  |


---

## ☁️ Architektura chmurowa (AWS)

### Schemat infrastruktury

![AWS Cloud Architecture Diagram](.github/Chattex_Cloud_Structure.jpg "AWS Cloud Architecture Diagram")

### Schemat CI/CD

![CI/CD pipeline graph](.github/ci_cd.png "CI/CD pipeline graph")

---

