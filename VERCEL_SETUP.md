# 🚀 Deploy OKComputer AI to Vercel - Step by Step

## ✅ What's Already Done
- ✅ Code pushed to GitHub: `https://github.com/dpsfeastcodinghere-a11y/okcomputer-ai-adaptive-tutor`
- ✅ Vercel configuration file (`vercel.json`) created
- ✅ Flask API configured for serverless deployment
- ✅ All dependencies listed in `requirements.txt`

---

## 📋 Deploy to Vercel in 5 Minutes

### **Step 1: Go to Vercel Dashboard**
1. Open your browser and go to: **[https://vercel.com](https://vercel.com)**
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"** (recommended)

---

### **Step 2: Import Your GitHub Repository**

1. Once logged in, click **"Add New..."** button (top right)
2. Select **"Project"**
3. You'll see a list of your GitHub repositories
4. Find **`okcomputer-ai-adaptive-tutor`** and click **"Import"**

   > **Don't see your repo?** Click "Adjust GitHub App Permissions" and grant access to the repository.

---

### **Step 3: Configure Project Settings**

Vercel will auto-detect most settings from your `vercel.json` file, but verify:

#### **Framework Preset:**
- Select: **"Other"** (since we have custom configuration)

#### **Root Directory:**
- Leave as: **`./`** (root)

#### **Build Settings:**
- **Build Command:** Leave empty (not needed for serverless)
- **Output Directory:** Leave empty
- **Install Command:** `pip install -r requirements.txt`

#### **Environment Variables:** (Optional - only if using real AI APIs)
- Click **"Add Environment Variable"**
- Add any API keys if needed (e.g., `QWEN_API_KEY`)

---

### **Step 4: Deploy!**

1. Click the big **"Deploy"** button
2. Wait 1-2 minutes while Vercel builds and deploys
3. You'll see a success screen with your live URL! 🎉

Your app will be live at: **`https://okcomputer-ai-adaptive-tutor.vercel.app`**

---

## 🔧 Post-Deployment Steps

### **Test Your Deployment**

Visit your deployed URL and test:
- ✅ Main page loads (`/` redirects to `/learning.html`)
- ✅ Dashboard page works (`/dashboard.html`)
- ✅ Progress page works (`/progress.html`)
- ✅ Student profile switching works
- ✅ Quiz functionality works
- ✅ API endpoints respond (check browser console)

### **Custom Domain (Optional)**

1. In Vercel dashboard, go to your project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain (e.g., `okcomputer.yourdomain.com`)
4. Follow DNS configuration instructions

---

## 🔄 Automatic Deployments

**Great news!** Now every time you push to GitHub, Vercel will automatically:
1. Detect the changes
2. Build and deploy
3. Give you a preview URL for each commit

To push updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

---

## 📊 Monitor Your Deployment

### **View Deployment Logs:**
1. Go to Vercel Dashboard
2. Click on your project
3. Click on any deployment
4. View **"Build Logs"** and **"Function Logs"**

### **Check Analytics:**
- Vercel provides free analytics
- See visitor stats, performance metrics, etc.

---

## 🐛 Troubleshooting

### **Issue: Build Failed**
- Check the build logs in Vercel dashboard
- Ensure `requirements.txt` has correct dependencies
- Verify Python version compatibility

### **Issue: API Routes Not Working**
- Check that `api/index.py` exists
- Verify `vercel.json` routes configuration
- Check function logs for errors

### **Issue: Static Files Not Loading**
- Ensure file paths in HTML are relative (not absolute)
- Check browser console for 404 errors
- Verify files are committed to Git

### **Issue: "This Serverless Function has crashed"**
- Check function logs in Vercel dashboard
- Verify Flask app imports correctly
- Check for Python syntax errors

---

## 🎯 Quick Links

- **Your GitHub Repo:** https://github.com/dpsfeastcodinghere-a11y/okcomputer-ai-adaptive-tutor
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support

---

## 🚀 Your Deployment Checklist

- [ ] Sign up/login to Vercel
- [ ] Import GitHub repository
- [ ] Configure project settings
- [ ] Click Deploy
- [ ] Test all pages and features
- [ ] Share your live URL!

---

## 📱 Share Your App

Once deployed, share your app:
- **Live URL:** `https://okcomputer-ai-adaptive-tutor.vercel.app`
- **GitHub:** `https://github.com/dpsfeastcodinghere-a11y/okcomputer-ai-adaptive-tutor`

---

## 🎉 You're All Set!

Your OKComputer AI Adaptive Tutor is ready to be deployed to the world!

**Need help?** Check the troubleshooting section or reach out with any questions.

**Happy Deploying! 🚀**
