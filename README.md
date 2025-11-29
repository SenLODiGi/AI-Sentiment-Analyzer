# 🧠 AI Sentiment Analyzer

A modern, responsive web application for sentiment analysis built with Python, NiceGUI, and TextBlob. Features both quick analysis and comprehensive deep analysis with beautiful glassmorphism UI design.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🔍 **Dual Analysis Modes**
- **Quick Analyze**: Fast sentiment scoring with key insights
- **Deep Analyze**: Comprehensive report with sentence-by-sentence analysis, word frequency, and advanced metrics

### 🎨 **Modern UI/UX**
- Beautiful glassmorphism design with gradient backgrounds
- Fully responsive layout for desktop, tablet, and mobile
- Bootstrap social media icons with hover effects
- Dark theme optimized for readability

### 📊 **Analysis Capabilities**
- Sentiment polarity scoring (-1 to +1)
- Subjectivity analysis (objective vs subjective)
- Key phrase extraction
- Word frequency analysis
- Sentence-by-sentence sentiment breakdown
- Emotional consistency scoring
- Text complexity metrics

### 👤 **Personal Branding**
- Integrated developer profile card
- Social media links (LinkedIn, YouTube, WhatsApp, Instagram)
- Professional presentation with profile image

### 📱 **Responsive Design**
- Mobile-first approach
- Adaptive grid layout
- Touch-friendly interface
- Optimized for all screen sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-sentiment-analyzer.git
   cd ai-sentiment-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (required for TextBlob)**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('punkt_tab')"
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8080`

## 📁 Project Structure

```
ai-sentiment-analyzer/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── image.png              # Profile image (replace with your own)
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── .venv/                 # Virtual environment (not tracked)
```

## 🛠️ Configuration

### Personal Profile Setup
**⚠️ IMPORTANT: Update these before deploying!**

Edit the configuration section in `main.py`:

```python
# ---------- CONFIG ----------
PROFILE_IMAGE = 'image.png'  # Replace with your profile image
NAME = "Your Full Name"      # Replace with your name
TITLE = "Your Professional Title"  # Replace with your title
LINKS = [
    ("LinkedIn", "https://linkedin.com/in/yourprofile", "bi-linkedin"),
    ("YouTube", "https://youtube.com/@yourchannel", "bi-youtube"), 
    ("WhatsApp", "https://wa.me/yourphonenumber", "bi-whatsapp"),
    ("Instagram", "https://instagram.com/yourusername", "bi-instagram"),
]
```

**📋 See `SETUP.md` for complete configuration checklist**

### Custom Styling
The application uses CSS variables for easy theming:
- `--accent-start`: Gradient start color
- `--accent-end`: Gradient end color
- `--glass`: Glass effect transparency

## 🌐 Deployment Options

### Option 1: Railway (Recommended for Python apps)
Railway provides excellent Python support:

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect Python and deploy
4. Set environment variables if needed

### Option 2: Render
Free Python hosting option:

1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Select "Web Service"
4. Configure build and start commands

### Option 3: Heroku
Traditional platform with Python support:

1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Deploy using Git

### Vercel Limitations
**Note**: Vercel is optimized for frontend frameworks and serverless functions. While possible to deploy Python apps, it's not ideal for NiceGUI applications that need a persistent server. Consider Railway or Render for better Python support.

## 📋 Requirements

### Python Dependencies
```
nicegui>=1.4.0
textblob>=0.19.0
nltk>=3.9
```

### System Requirements
- Python 3.8+
- 512MB RAM minimum
- Internet connection (for NLTK downloads)

## 🎯 Usage Examples

### Quick Analysis
Perfect for:
- Social media posts
- Customer reviews
- Email content
- Chat messages

### Deep Analysis
Ideal for:
- Long-form content
- Articles and blogs
- Academic papers
- Marketing copy

## 🔧 Development

### Local Development
1. Install dependencies in development mode
2. Make your changes
3. Test locally with `python main.py`
4. Commit and push to GitHub

### Adding Features
- Modify the analysis functions in `main.py`
- Update UI components using NiceGUI syntax
- Add new CSS styles in the head section

## 📊 Technology Stack

- **Backend**: Python 3.8+
- **Web Framework**: NiceGUI
- **NLP Library**: TextBlob + NLTK
- **Frontend**: HTML/CSS/JavaScript (via NiceGUI)
- **Styling**: Custom CSS with Bootstrap Icons
- **Deployment**: Railway/Render recommended

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you have any questions or need help:
- Open an issue on GitHub
- Contact via social media links in the app
- Check the NiceGUI documentation

## 🚀 Live Demo

Try the live application: [Your Deployed URL Here]

---

**Built with ❤️ by Senith Samaranayake**

*Digital Marketer | Growth Strategist | Personal Development Speaker*

*Powered by NiceGUI, TextBlob, and Python*
5. Vercel auto-detects Python and deploys!

### Deploy to Render
1. Push this repo to GitHub
2. Go to [Render.com](https://render.com)
3. Create new "Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **Web Framework** | NiceGUI (FastAPI + Vue3) | Pure Python, beautiful UI, zero config |
| **Sentiment Engine** | VADER Sentiment | Industry-standard, no training required |
| **UI Framework** | Tailwind CSS | Modern, responsive design |
| **Deployment** | Vercel/Railway/Render | One-click deploy, zero config |

## 🎨 Why This Stack?

- **No JavaScript/TypeScript** - Pure Python developers can build modern web apps
- **Zero Build Steps** - No webpack, no npm, no package.json
- **Beautiful by Default** - Modern UI with gradients, blur effects, animations
- **Professional Performance** - FastAPI backend is production-ready
- **Easy Deploy** - Works on all major Python hosting platforms

## 📁 Project Structure

```
social-sentiment-reader-python/
├── main.py              # ← Everything in this one file!
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚀 Advanced Usage

The app is designed to be easily extensible. Want to add features like:


