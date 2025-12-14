# 🎓 OKComputer AI Adaptive Tutor

An intelligent, adaptive learning platform powered by lightweight AI for personalized education.

## ✨ Features

- 🤖 **AI-Powered Learning** - Uses Hugging Face FLAN-T5 (lightweight, open-source)
- 👥 **Student Profiles** - Ram (Foundational) & Rahul (Advanced)
- 📚 **Full Syllabus** - Math, Science, English, Social Studies (Classes 6-10)
- ♿ **Accessible** - Screen reader support, keyboard navigation
- 🎯 **Adaptive** - Adjusts difficulty based on performance

## 🚀 Quick Start

### 1. Get Hugging Face API Key (FREE)

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `okcomputer-ai`
4. Type: **Read** (recommended) or Write
5. Click "Create token"
6. Copy the token (starts with `hf_...`)

### 2. Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/dpsfeastcodinghere-a11y/okcomputer-ai-adaptive-tutor)

1. Click the button above
2. Sign in with GitHub
3. Add environment variable:
   - **Name:** `HUGGINGFACE_API_KEY`
   - **Value:** `hf_your_token_here` (paste your token)
4. Click "Deploy"

### 3. Test Locally (Optional)

```bash
# Clone the repository
git clone https://github.com/dpsfeastcodinghere-a11y/okcomputer-ai-adaptive-tutor.git
cd okcomputer-ai-adaptive-tutor

# Install dependencies
pip install -r requirements.txt

# Set environment variable (Windows PowerShell)
$env:HUGGINGFACE_API_KEY="hf_your_token_here"

# Run the app
python api.py
```

Visit: http://localhost:5000

## 📖 Documentation

- [AI Integration Guide](AI_INTEGRATION_GUIDE.md) - Complete AI setup
- [Deployment Guide](VERCEL_SETUP.md) - Step-by-step deployment
- [Features Summary](FEATURES_SUMMARY.md) - All features listed
- [FAQ](FAQ.md) - Common questions answered

## 🤖 AI Model

**Model:** google/flan-t5-small
- **Size:** 77M parameters (lightweight!)
- **License:** Apache 2.0 (Open Source)
- **Cost:** FREE tier (30,000 chars/month)
- **Speed:** Fast (1-2 seconds)
- **GPU:** Not required

## 🎯 Student Profiles

### Ram (Foundational)
- Guided learning
- Step-by-step explanations
- Encouraging feedback
- Easier questions

### Rahul (Advanced)
- Fast-paced learning
- Challenging problems
- Strict checking
- Advanced concepts

## ♿ Accessibility

- **Keyboard Shortcuts:**
  - `Alt + 1` - Quiz Mode
  - `Alt + 2` - Concept Notes
  - `Alt + 3` - Ask EduAI
  - `Alt + P` - Change Profile
  - `Alt + H` - Show Help

- **Screen Reader:** Full ARIA support
- **Focus Indicators:** Clear visual feedback
- **Skip Links:** Quick navigation

## 📚 Syllabus Coverage

### Subjects
- Mathematics (Classes 6-10)
- Science (Classes 6-10)
- English (Classes 6-10)
- Social Studies (Classes 6-10)

### Content
- 300+ questions with solutions
- Multiple difficulty levels
- Hints and explanations
- Adaptive learning paths

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **AI:** Hugging Face FLAN-T5
- **Deployment:** Vercel
- **Styling:** Tailwind CSS

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ for adaptive learning**
