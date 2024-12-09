# 📚 Paper Pulse

<div align="center">

![Paper Pulse Logo](figures/Screenshot%202024-12-09%20140807.png)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)


*An AI-powered research paper digest tool that helps you stay on top of the latest academic publications*

[Features](##features) • [Installation](##installation) • [Usage](#usage) • [Roadmap](#roadmap) • [Contributing](#contributing)
</div>

## 🌟 Features

- 🔍 **Smart Search**: Find relevant papers across multiple categories on arXiv
- 🤖 **AI-Powered Summaries**: Automatically generate structured summaries using LLaMA 3
- 📊 **Clean Interface**: Modern, responsive web interface for easy paper browsing
- 📝 **Structured Analysis**: Break down papers into motivation, method, results, and impact
- ⚡ **Real-time Updates**: Access papers published within the last 24 hours

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Hasnat79/PaperPulse
cd PaperPulse

# Create and activate virtual environment
conda create -n paper_pulse python=3.10  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

## 💻 Usage

1. Start the server:
```bash
cd src
python main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Enter your research keywords in the search bar

4. Browse through motivation, method, results, and impact of the latest papers

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **AI Model**: LLaMA 3 (8B Instruct) via Replicate
- **Paper Source**: arXiv API
- **Frontend**: HTML, CSS
- **Styling**: Custom CSS with responsive design


## 🗺️ Roadmap

- [ ] Automated email digests via cron jobs
- [ ] LinkedIn paper traction tracking
- [ ] Integration with ACM Digital Library
- [ ] Integration with IEEE Xplore
- [ ] Local background execution with daily updates
- [ ] Enhanced summary generation


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- arXiv for providing access to research papers
- Replicate AI for the LLaMA 3 model access
- The FastAPI team for the amazing framework

---

<div align="center">
Made with ❤️ by Hasnat79

⭐️ Star this repo if you find it helpful!
</div>
