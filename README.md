# 🎮 GameLib

### Junior Full Stack Web Developer · React · TypeScript · Python · Django · PostgreSQL · Docker

**GameLib is a full-stack web application that I designed, developed and deployed as a portfolio project.**

It allows users to search for videogames, create an account and manage their own personal library.

🌐 **Live Demo:** https://gamelib.pipayplata.com
💻 **GitHub:** https://github.com/Pilar84/GameLib

---

## 👩‍💻 About Me

Hi, I'm **Pilar Girón**, a **Junior Full Stack Web Developer** with a Higher Technician degree in **Web Application Development (DAW)**.

I enjoy building complete web applications, from the user interface and REST APIs to databases, Docker containers and production deployment.

### My main technologies

**Frontend**

* React
* TypeScript
* JavaScript
* HTML5 / CSS3
* Bootstrap

**Backend**

* Python
* Django
* REST APIs

**Data**

* PostgreSQL
* SQL
* Redis

**Tools & Deployment**

* Docker
* Docker Compose
* Git / GitHub
* Linux
* Nginx

I'm currently **Open to Work** and looking for my first opportunity as a **Junior Full Stack Web Developer**.

---

## 🚀 What I Built

GameLib is a complete web application rather than a standalone frontend project.

### 🔎 Videogame catalogue

Users can search for videogames and access their available information.

### 👤 Authentication

The application includes:

* User registration
* Login
* Logout
* Session management
* Password change
* Account deletion

### 📚 Personal library

Each authenticated user has their own videogame library.

The backend ensures that the same videogame cannot be added twice by the same user, while allowing different users to have the same game in their libraries.

### 📱 Responsive interface

The application is designed to work on desktop and mobile devices.

---

## 🏗️ Full Stack Architecture

```text
                 USER
                   │
                   ▼
        ┌─────────────────────┐
        │ React + TypeScript  │
        │       Vite          │
        └──────────┬──────────┘
                   │
                 REST API
                   │
                   ▼
        ┌─────────────────────┐
        │ Django + Python     │
        │      Gunicorn       │
        └───────┬───────┬─────┘
                │       │
                ▼       ▼
         PostgreSQL    Redis
```

The complete application is containerised with **Docker** and deployed to a real **Linux VPS**.

---

## 🐳 Production Deployment

One of the main goals of this project was not only to develop the application, but also to make it available online.

The production environment includes:

* Ubuntu VPS
* Docker
* Docker Compose
* Nginx
* Django + Gunicorn
* PostgreSQL
* Redis
* HTTPS

### 🌐 Try the application

**https://gamelib.pipayplata.com**

---

## 💡 What This Project Shows

Through GameLib I have worked on:

* Full Stack web development
* React component development
* TypeScript
* REST API integration
* Django backend development
* Authentication and user management
* PostgreSQL database design
* Data validation
* Error handling
* Docker
* Linux deployment
* Nginx configuration
* Git and GitHub

---

## 📂 Project Structure

```text
GameLib/
│
├── Steamlike-frontend/      # React + TypeScript
├── auth_api/                # Authentication API
├── library/                 # User videogame library
├── steamlike_backend/       # Django configuration
│
├── Dockerfile
├── docker-compose.prod.yml
└── manage.py
```

The internal `Steamlike` names are retained from the original development stage. The project is publicly presented as **GameLib**.

---

## 📌 Project Status

🟢 **Live and deployed**

This project is part of my professional portfolio and demonstrates my ability to develop and deploy a complete web application.

---

## 👩‍💻 Pilar Girón

**+34 651885750

**pilargijor@hotmail.es

**Junior Full Stack Web Developer**

**Open to Work · Immediate Availability**

📍 Córdoba, Spain

💻 GitHub: https://github.com/Pilar84
🌐 GameLib: https://gamelib.pipayplata.com
