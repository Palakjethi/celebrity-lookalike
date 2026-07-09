
# 🎬 Celebrity Lookalike Finder

> **Find your celebrity twin in seconds** — powered by ArcFace AI across 843+ Bollywood & Hollywood celebrities.

<img width="1920" height="1080" alt="Screenshot (167)" src="https://github.com/user-attachments/assets/b2ce371f-5279-4805-84b6-d80433ee80e3" />



---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **AI Face Matching** | ArcFace deep learning model with 512-d embeddings |
| 🌍 **Bollywood + Hollywood** | 843+ celebrities indexed |
| 👤 **Gender Filter** | Match with Male / Female / Any |
| 🎬 **Industry Filter** | Bollywood only / Hollywood only / Both |
| 📊 **Feature Breakdown** | See similarity across eyes, jawline, nose, face shape |
| 📤 **Share Card** | Download and share your result on WhatsApp & Twitter |
| 🔒 **Privacy First** | Zero photos stored — deleted immediately after matching |

---

## 🖥️ Demo

<img width="1920" height="1080" alt="Screenshot (167)" src="https://github.com/user-attachments/assets/b2ce371f-5279-4805-84b6-d80433ee80e3" />



### Results Page

<img width="1920" height="1080" alt="Screenshot (169)" src="https://github.com/user-attachments/assets/6c4b5db7-add2-4888-bd3b-5b2dcf63cb86" />
<img width="1920" height="1080" alt="Screenshot (169)" src="https://github.com/user-attachments/assets/6682ab38-1ff2-473d-b20c-95b0c4c04ce3" />


---

## 🧠 How It Works

1. Upload your photo or use webcam
2. ArcFace extracts a 512-dimensional face embedding
3. FAISS searches through 843 celebrity embeddings
4. Results show side-by-side comparison with confidence scores
5. Share your result on social media

---

## 🛠️ Tech Stack

### Frontend
- ⚛️ React + Vite
- 🎨 CSS Modules
- 📡 Axios

### Backend
- ⚡ FastAPI
- 🤖 DeepFace + ArcFace
- 🔍 FAISS vector search
- 🖼️ TMDB API for celebrity photos

### Infrastructure
- 🌐 Frontend → Vercel
- 🖥️ Backend → Hugging Face Spaces
- 📸 Celebrity Photos → TMDB CDN

---

## 🚀 Live Demo

🌍 **[Try it live →](https://celebrity-lookalike-nine.vercel.app)**

---

## 📦 Local Setup

```bash
# Clone the repo
git clone https://github.com/Palakjethi/celebrity-lookalike

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn api:app --reload

# Run the frontend
cd frontend
npm install
npm run dev
```

---

## 📊 Dataset

- **Source:** TMDB API (The Movie Database)
- **Size:** 843 celebrities, ~3000 photos
- **Coverage:** Hollywood + Bollywood
- **Embedding model:** ArcFace (512-dimensional vectors)
- **Vector index:** FAISS IndexFlatIP (cosine similarity)

---

## 🔒 Privacy

Your photos are **never stored**. Each uploaded image is:
1. Temporarily saved in memory
2. Processed for face embedding
3. Immediately deleted
4. Never logged or retained

---

## 👩‍💻 Author

**Palak Jethi**
- GitHub: [@Palakjethi](https://github.com/Palakjethi)

---

⭐ Star this repo if you found your celebrity twin!
