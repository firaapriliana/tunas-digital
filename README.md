# 🌱 TUNAS Digital — Agentic Chatbot Edukasi Perlindungan Anak

Aplikasi Streamlit untuk edukasi perlindungan anak di ruang digital dengan AI agent yang cerdas.

## ✨ Features

- 🤖 **AI Agent** yang dapat membaca PDF regulasi
- 📚 **Pencarian Informasi** terbaru dari internet
- 💬 **Chat Interface** yang user-friendly
- 🎨 **Custom Design** dengan CSS menarik
- 📱 **Responsive** design untuk mobile

## 🚀 Quick Deploy

### Option 1: Streamlit Cloud (Easiest)

```bash
# 1. Push ke GitHub
git push origin main

# 2. Go to https://streamlit.io/cloud
# 3. Select repo dan deploy
# 4. Add secrets: GOOGLE_API_KEY, EXA_API_KEY
```

**Live in 5 minutes!** ✅

### Option 2: Railway (Best Performance)

```bash
# 1. Go to https://railway.app
# 2. Create new project dari GitHub
# 3. Add environment variables
# 4. Auto-deploy!
```

### Option 3: Hugging Face Spaces

```bash
# 1. Create new Space di https://huggingface.co/spaces
# 2. Upload files
# 3. Add secrets
# 4. Auto-deploy!
```

## 🔧 Local Development

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/tunas-digital-agentic.git
cd tunas-digital-agentic

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your_key"
export EXA_API_KEY="your_key"

# Run app
streamlit run streamlit_app.py
```

## 🔑 Environment Variables

Add to hosting platform secrets:

```
GOOGLE_API_KEY=your_google_api_key
EXA_API_KEY=your_exa_api_key
```

## 📖 Architecture

- **Frontend**: Streamlit (Python)
- **AI Agent**: LangChain + Google GenAI
- **PDF Processing**: PyPDF2
- **Web Search**: EXA API
- **Hosting**: Streamlit Cloud / Railway / HF Spaces

## 📊 Performance

- **Load Time**: < 2 seconds
- **Chat Response**: 2-5 seconds
- **Concurrent Users**: 50+ (Streamlit Cloud)
- **Uptime**: 99%+ (SLA)

## 🆘 Troubleshooting

### "Module not found"
→ Check `requirements.txt` has all packages

### "API key not found"
→ Add to platform secrets, not code

### "App too slow"
→ Try Railway for better performance

### "PDF not loading"
→ Check file size < 200MB

## 📝 License

MIT License - Perlindungan Anak Indonesia

## 🤝 Contributing

Kontribusi welcome! 
- Fork repo
- Create feature branch
- Make pull request

## 📞 Support

Issues atau questions? Buat GitHub issue.

---

**🌱 Melindungi Anak Indonesia di Ruang Digital 🌱**

Made with ❤️ untuk Indonesia
