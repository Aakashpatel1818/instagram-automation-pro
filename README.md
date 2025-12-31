# 📱 Instagram Automation Pro

**Professional Instagram DM & Comment Automation App** built with React + Python FastAPI

> Automate Instagram comments and DMs with intelligent toggle features. Control whether to send only comments, or comments + automatic DMs.

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![React](https://img.shields.io/badge/React-18%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Core Features

- **Smart Comment Automation** - Auto-reply to Instagram comments with keyword triggers
- **Toggle System 🔥** - Choose between Comment-Only or Comment + Auto DM
- **Admin Dashboard** - Beautiful React interface to manage automation rules
- **Real-time Logs** - Track all comments and DMs sent
- **Lead Capture** - Capture and organize leads from DMs
- **Meta OAuth Integration** - Secure authentication with Instagram

## 🏗️ Tech Stack

**Frontend:** React 18 + Vite + TypeScript + Tailwind CSS
**Backend:** Python FastAPI + MongoDB + Async/Await
**Database:** MongoDB Atlas
**Authentication:** JWT + Meta OAuth

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- MongoDB Atlas account
- Meta Developer account

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## 📚 Documentation

- [Setup Guide](./docs/SETUP.md)
- [API Documentation](./docs/API.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

---

## 🔧 Toggle Feature

Every automation rule has two toggles:

**Comment Only Mode:**
- Reply to comment ✓
- Don't send DM

**Comment + DM Mode:**
- Reply to comment ✓
- Send automatic DM ✓

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**Aakash Patel**
- GitHub: [@Aakashpatel1818](https://github.com/Aakashpatel1818)
- Location: Bärdoli, Gujarat, India

Made with ❤️ for Instagram automation enthusiasts