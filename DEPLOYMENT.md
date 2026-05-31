# Deployment Guide

## Overview
This project contains two separate deployable parts:

- `backend/`: Flask API service
- `frontend/`: React + Vite web app

The backend is already configured for deployment using Railway via `nixpacks.toml`.
The frontend can be deployed as a static site to Netlify, Vercel, or any static-hosting provider.

---

## Backend Deployment (Recommended: Railway)

### 1. Push code to GitHub

Create a GitHub repository and push the `recommendation-system` folder.

### 2. Create a Railway project

1. Go to Railway and create a new project.
2. Add a new service and connect the repository to `recommendation-system/backend`.
3. Railway detects the Python app and uses `nixpacks.toml`.
4. Set the start command if it is not auto-detected:

```bash
gunicorn run:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

### 3. Add a MySQL database

1. Add the Railway MySQL plugin to the project.
2. Copy the database credentials into these environment variables in the Railway service settings:

- `MYSQLHOST`
- `MYSQLPORT`
- `MYSQLUSER`
- `MYSQLPASSWORD`
- `MYSQLDATABASE`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

Example values:

```text
SECRET_KEY=replace-with-a-long-secret
JWT_SECRET_KEY=replace-with-a-long-secret
MYSQLHOST=<railway-host>
MYSQLPORT=<railway-port>
MYSQLUSER=<railway-user>
MYSQLPASSWORD=<railway-password>
MYSQLDATABASE=<railway-database>
```

### 4. Initialize the database schema

Use a MySQL client or Railway connection to run the SQL schema file:

```bash
mysql -h $MYSQLHOST -P $MYSQLPORT -u $MYSQLUSER -p $MYSQLPASSWORD $MYSQLDATABASE < backend/database/schema.sql
```

### 5. Seed initial data

Run the seed script from the backend service environment:

```bash
python seed_railway.py
```

That creates example movies, music, books, and an admin user.

---

## Frontend Deployment (Recommended: Netlify or Vercel)

### 1. Build the frontend

From `recommendation-system/frontend`:

```bash
npm install
npm run build
```

### 2. Deploy the static site

Use Netlify, Vercel, or any static site host. Configure the publish directory to `dist`.

### 3. Configure API URL

Set the environment variable for production:

```text
VITE_API_URL=https://<your-backend-domain>/api
```

The frontend already uses this variable in `src/services/api.js`.

---

## Alternative: Deploy Frontend as Railway Service

If you want both backend and frontend on Railway, create a second service for the frontend:

- Root path: `recommendation-system/frontend`
- Build command: `npm install && npm run build`
- Start command: `npx serve -s dist --listen $PORT`
- Set `VITE_API_URL` to the backend URL and rebuild.

Note: `serve` can be installed automatically at runtime by Railway if needed.

---

## Local Production Testing

### Backend

```bash
cd recommendation-system/backend
pip install -r requirements.txt
python run.py
```

### Frontend

```bash
cd recommendation-system/frontend
npm install
npm run dev
```

Then open `http://localhost:3000`.

---

## Files Added

- `backend/.env.example`
- `frontend/.env.example`
- `DEPLOYMENT.md`
