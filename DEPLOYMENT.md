# 🚀 OKComputer AI Adaptive Tutor - Deployment Guide

## Quick Deploy to Vercel (Recommended - FREE)

### Prerequisites
1. A [Vercel account](https://vercel.com/signup) (free)
2. [Git](https://git-scm.com/downloads) installed
3. [Vercel CLI](https://vercel.com/docs/cli) (optional, but recommended)

### Method 1: Deploy via Vercel CLI (Fastest)

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Login to Vercel
```bash
vercel login
```

#### Step 3: Deploy
Navigate to your project directory and run:
```bash
cd "c:\Users\ashwi_rna9dpj\Downloads\OKComputer_AI Adaptive Tutor"
vercel
```

Follow the prompts:
- **Set up and deploy?** → Yes
- **Which scope?** → Select your account
- **Link to existing project?** → No
- **Project name?** → okcomputer-ai-tutor (or your preferred name)
- **Directory?** → ./ (current directory)
- **Override settings?** → No

Your app will be deployed! You'll get a URL like: `https://okcomputer-ai-tutor.vercel.app`

#### Step 4: Production Deployment
For production deployment:
```bash
vercel --prod
```

---

### Method 2: Deploy via Vercel Dashboard (No CLI Required)

#### Step 1: Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new)
2. Initialize git in your project (if not already done):
```bash
cd "c:\Users\ashwi_rna9dpj\Downloads\OKComputer_AI Adaptive Tutor"
git init
git add .
git commit -m "Initial commit - OKComputer AI Adaptive Tutor"
```

3. Add remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

#### Step 2: Import to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Vercel will auto-detect the settings from `vercel.json`
5. Click **"Deploy"**

---

## Alternative Hosting Options

### Option 2: Render (Free Tier Available)

1. Create account at [Render](https://render.com)
2. Create a new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`
   - **Environment**: Python 3

### Option 3: Railway (Easy Full-Stack Deployment)

1. Go to [Railway](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Railway will auto-detect and deploy

### Option 4: PythonAnywhere (Python-Focused)

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your files
3. Configure WSGI file to point to your Flask app
4. Set up static file mappings

---

## Local Testing (Before Deployment)

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask backend
python api.py
```

Then open `learning.html` in your browser or use a local server:
```bash
# Using Python's built-in server
python -m http.server 8000
```

Visit: `http://localhost:8000/learning.html`

---

## Environment Variables (If Needed)

If you plan to integrate real AI APIs (like Qwen), add these to your Vercel project:

1. Go to your project settings on Vercel
2. Navigate to **Environment Variables**
3. Add:
   - `QWEN_API_KEY` = your_api_key
   - `FLASK_ENV` = production

---

## Troubleshooting

### Issue: API routes not working
- Ensure `api/index.py` correctly imports the Flask app
- Check that `vercel.json` routes are configured properly

### Issue: Static files not loading
- Verify file paths in HTML are relative (not absolute)
- Check `vercel.json` routes include all file extensions

### Issue: Python dependencies failing
- Ensure `requirements.txt` is in the root directory
- Use compatible versions (Flask 3.0.0 works well)

---

## Post-Deployment Checklist

- [ ] Test all pages (learning.html, dashboard.html, progress.html)
- [ ] Verify API endpoints (/api/validate-answer, /api/solve-doubt)
- [ ] Check student profile switching functionality
- [ ] Test quiz generation and doubt solver
- [ ] Verify responsive design on mobile devices

---

## Custom Domain (Optional)

After deployment, you can add a custom domain:
1. Go to your Vercel project settings
2. Navigate to **Domains**
3. Add your custom domain
4. Update DNS records as instructed

---

## Support

For issues or questions:
- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Project Issues: Create an issue in your GitHub repo

---

**Ready to deploy?** Start with Method 1 (Vercel CLI) for the fastest deployment! 🚀
