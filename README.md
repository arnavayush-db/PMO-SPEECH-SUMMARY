# 🇮🇳 PMO Speech Synthesis (Text-Only AI Project)

A full-stack AI-powered platform that **automatically collects**, **summarizes**, and **presents Prime Minister of India's speeches** in a simplified, readable text format. Designed for students, researchers, and the general public, this tool uses Python, Angular, FastAPI, and MySQL to make public speeches more accessible.

> ❗ **Note**: This project **does not include audio or speech playback** — only **text-based summarization**.

---

## 📌 Features

- 🕸️ **Web Scraping**: Fetches PM speeches from official government sources.
- 🤖 **AI Summarization**: Uses LLMs like GPT or Grok to generate short summaries.
- 🧑‍💻 **Frontend UI**: Built with Angular for a clean and responsive interface.
- ⚙️ **Backend API**: Powered by FastAPI to handle data and logic.
- 🗃️ **MySQL Database**: Stores full and summarized texts with metadata.
- 🚀 **Deployment Ready**: Compatible with GitHub Pages (frontend).

---

## 🧠 Why This Project?

PM speeches often contain dense and formal language. Citizens and students may find it hard to digest. This platform simplifies those speeches by summarizing key points, improving understanding, and promoting transparency.

---

## 🧩 Project Structure

PMO-SPEECH-SYNTHESIS/
│
├── frontend/ # Angular app (UI)
├── backend/ # FastAPI server (API + summarization)
├── crawler/ # Web scraper scripts
├── database/ # SQLite schema and setup
├── .nojekyll # Disables Jekyll for GitHub Pages
├── README.md # Project documentation
└── requirements.txt # Python backend dependencies

---

## 🛠️ Technologies Used

| Layer       | Tools & Languages                        |
|-------------|------------------------------------------|
| Frontend    | Angular, TypeScript, HTML, CSS           |
| Backend     | Python, FastAPI                          |
| Database    | Sqlite                                 |
| Scraping    | BeautifulSoup, requests                  |
| AI/NLP      | OpenAI GPT / Grok LLM (for summaries)    |
| Hosting     | GitHub Pages (frontend only)             |

---

## 🚀 How to Run the Project Locally

### 1️⃣ Clone the Repository

git clone https://github.com/arnavayush-db/PMO-SPEECH-SYNTHESIS.git
cd PMO-SPEECH-SYNTHESIS
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
cd .\frontend\
npm install
ng serve
Visit http://localhost:4200 to view the app. in any Search Engine 
![image alt](https://github.com/arnavayush-db/PMO-SPEECH-SUMMARY/blob/98c5c0262db68f4389411a7a813a59a46149c5f2/Screenshot%202025-05-22%20150033.png)

--Arnav Ayush--
Final Year BCA Student
RKDF University, Ranchi
GitHub: arnavayush-db

