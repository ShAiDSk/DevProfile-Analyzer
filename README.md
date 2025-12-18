<div align="center">

  <img src="https://readme-typing-svg.herokuapp.com?font=Space+Grotesk&weight=700&size=40&pause=1000&color=A855F7&center=true&vCenter=true&width=600&lines=DevProfile+Analyzer;Code+Analysis+x+AI+Roasts;Analyze.+Roast.+Hype.+Repeat.;Built+with+Flask+%26+Groq+AI" alt="Typing SVG" />

  <h3 align="center">⚡ The Ultimate Developer Portfolio Analyzer ⚡</h3>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
    <img src="https://img.shields.io/badge/AI-Groq_Llama3-F05032?style=for-the-badge&logo=openai&logoColor=white" />
    <a href="https://github.com/ShAiDSk/DevProfile-Analyzer/stargazers">
      <img src="https://img.shields.io/github/stars/ShAiDSk/DevProfile-Analyzer?style=for-the-badge&color=yellow" />
    </a>
    <a href="https://github.com/ShAiDSk/DevProfile-Analyzer/issues">
      <img src="https://img.shields.io/github/issues/ShAiDSk/DevProfile-Analyzer?style=for-the-badge&color=red" />
    </a>
  </p>

  <br/>
  
  <p>
    <a href="#-demo">View Demo</a> •
    <a href="#-features">Key Features</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </p>
</div>

---

### 🚀 Overview

**DevProfile Analyzer** is a full-stack web application that gamifies developer portfolios. By aggregating data from **Codeforces**, **LeetCode**, **GitHub**, **AtCoder**, and **CodeChef**, it generates a comprehensive "Developer Persona Card."

But we didn't stop there. We integrated **Groq AI (Llama 3)** to provide real-time, savage **Roasts** or inspiring **Hype** speeches based on your actual coding statistics.

### 🎥 Demo & Screenshots

<div align="center">
  <table>
    <tr>
      <td align="center"><b>🔥 The Dashboard</b></td>
      <td align="center"><b>🤖 AI Roasting</b></td>
    </tr>
    <tr>
      <td><img src="https://i.imgur.com/PLACEHOLDER_DASHBOARD.png" width="400" alt="Dashboard" /></td>
      <td><img src="https://i.imgur.com/PLACEHOLDER_ROAST.png" width="400" alt="AI Roast" /></td>
    </tr>
  </table>
</div>

---

### ✨ Features

| Feature | Description |
| :--- | :--- |
| **🐙 Multi-Platform Support** | Fetches live data from **Codeforces**, **LeetCode**, **GitHub**, **AtCoder**, and **CodeChef**. |
| **🤖 AI Integration** | Uses **Groq API (Llama-3-70b)** to generate funny roasts or motivational feedback based on stats. |
| **📊 Visual Analytics** | Interactive **Chart.js** graphs showing rating history and language distribution. |
| **🃏 Persona Engine** | Calculates a "Power Level" and assigns RPG-style classes (e.g., *Bug Hunter*, *Grandmaster*). |
| **📸 Shareable Cards** | Built-in `html2canvas` functionality to download a high-quality PNG of your stats. |
| **⚡ Glassmorphism UI** | A stunning, modern interface built with **Tailwind CSS** and custom animations. |

---

### 🛠 Tech Stack

<details>
  <summary><b>Click to expand Tech Stack details</b></summary>

  <br />

  | Component | Technology | Utility |
  | :--- | :--- | :--- |
  | **Backend** | Python (Flask) | REST API, Routing, Data Scraping |
  | **Frontend** | HTML5, JavaScript | Dynamic DOM manipulation, Fetch API |
  | **Styling** | Tailwind CSS | Responsive design, Animations, Glassmorphism |
  | **AI Engine** | Groq SDK | Ultra-fast LLM inference (Llama 3) |
  | **Visuals** | Chart.js | Data visualization |
  | **Deployment** | Render / Gunicorn | Production server hosting |

</details>

---

### ⚡ Installation

Follow these steps to set up the project locally.

#### 1. Clone the Repository
```bash
git clone [https://github.com/ShAiDSk/DevProfile-Analyzer.git](https://github.com/ShAiDSk/DevProfile-Analyzer.git)
cd DevProfile-Analyzer

```

#### 2. Set up Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your API Key:

```ini
# Get your free key at [https://console.groq.com/keys](https://console.groq.com/keys)
GROQ_API_KEY=gsk_your_api_key_here

```

#### 5. Run the Application

```bash
python app.py

```

> The app will start at `http://127.0.0.1:5000`

---

### 📂 Project Structure

```bash
DevProfile-Analyzer/
├── static/
│   ├── css/
│   │   └── style.css       # Custom animations & glass effects
│   └── js/
│       └── script.js       # Frontend logic, charts, & API calls
├── templates/
│   ├── index.html          # Main dashboard
│   └── navbar.html         # Modular navbar component
├── app.py                  # Main Flask application & Scrapers
├── .env                    # API Keys (Not shared)
├── requirements.txt        # Python dependencies
├── Procfile                # Render Deployment Config
└── README.md               # Documentation

```

---

### 🔮 Future Roadmap

* [ ] **Compare Mode:** Battle two profiles against each other.
* [ ] **Twitter Bot:** Auto-tweet your roasting results.
* [ ] **Streak Tracking:** Heatmap for daily coding activity.
* [ ] **Dark/Light Mode:** Toggle themes.

---

### 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
<p>Built with ❤️ by <a href="https://www.google.com/search?q=https://github.com/ShAiDSk">ShAiDSk</a></p>
<p>
<a href="https://www.google.com/search?q=https://github.com/ShAiDSk">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/GitHub-100000%3Fstyle%3Dfor-the-badge%26logo%3Dgithub%26logoColor%3Dwhite" />
</a>
</p>
</div>

```

```