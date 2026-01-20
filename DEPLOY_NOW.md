# 🚀 Deploy Tabsirah to Render - Quick Guide

Your project is ready for deployment! Follow these steps:

---

## ✅ Already Done (by script)

- [x] Updated `requirements.txt` with production dependencies
- [x] Created `Procfile` for Render
- [x] Created `.gitignore` (excludes large dataset, keeps models)
- [x] Created initial Git commit (52 files including models)

---

## 📋 Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name**: `tabsirah` (or any name you like)
   - **Description**: `Arabic Sign Language Quran Learning App`
   - **Visibility**: Public (recommended for free Render) or Private
3. **DO NOT** check "Add a README" (you already have one)
4. Click **Create repository**

---

## 📋 Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show you commands. Run these in your terminal:

```powershell
cd "C:\Users\huhul\Desktop\ArASL_Project - Copy"

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tabsirah.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example** (if your username is `huhul`):
```powershell
git remote add origin https://github.com/huhul/tabsirah.git
git push -u origin main
```

---

## 📋 Step 3: Deploy to Render

1. Go to **https://render.com**
2. Click **Sign Up** → Sign up with **GitHub** (easiest)
3. Click **New** → **Web Service**
4. Click **Connect** next to your `tabsirah` repository

5. Configure your service:
   | Setting | Value |
   |---------|-------|
   | **Name** | `tabsirah` |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn --chdir web_app app:app` |
   | **Instance Type** | `Free` |

6. Click **Create Web Service**

---

## 📋 Step 4: Wait for Deployment

Render will:
1. Clone your repository
2. Install dependencies (may take 5-10 minutes first time)
3. Start your Flask app
4. Give you a public URL like: `https://tabsirah.onrender.com`

---

## 🎉 Done!

After deployment, you'll have a **shareable link** that works on any device!

**Note**: Free tier sleeps after 15 min of inactivity. First visit after sleep takes ~30 seconds to wake up.

---

## 🔧 Troubleshooting

### If deployment fails with MediaPipe error:
The `opencv-python-headless` in requirements.txt should fix this. If not, try adding to requirements.txt:
```
--extra-index-url https://google-coral.github.io/py-repo/
```

### If camera doesn't work:
Make sure you're accessing via HTTPS (Render provides this automatically).

### If models don't load:
Check that `models/` folder was pushed to GitHub (it should be ~26MB total).

---

## 📞 Need Help?

Check Render documentation: https://render.com/docs/deploy-flask
