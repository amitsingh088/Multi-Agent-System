# 🤖 Multi-Agent Research System

A powerful AI-powered **Multi-Agent Research Assistant** built using **LangChain**, **LangGraph**, **OpenAI/Groq LLMs**, **Tavily Search API**, and **Streamlit**.

The application automatically researches a topic using multiple AI agents, generates a structured research report, and critiques the report for quality.

---

## 🚀 Live Demo

**🌐 Live Demo:**  
https://multi-agent-system-dsej6hznazynsc4ugrpjds.streamlit.app/

**💻 GitHub Repository:**  
https://github.com/amitsingh088/Multi-Agent-System

---

## 📌 Features

- 🔍 AI Search Agent for web research
- 📄 Reader Agent for webpage scraping
- ✍️ Research Writer Agent
- 🧠 Research Critic Agent
- 🌐 Real-time web search using Tavily API
- 📊 Clean Streamlit User Interface
- ⚡ Modular LangChain architecture
- 🔄 Easily switch between OpenAI and Groq models

---

## 🏗️ Architecture

```
               User Query
                    │
                    ▼
          Search Agent (Tavily)
                    │
                    ▼
          Reader Agent (Scraper)
                    │
                    ▼
         Research Writer Agent
                    │
                    ▼
         Research Critic Agent
                    │
                    ▼
            Final Research Report
```

---

## 🛠️ Tech Stack

- Python
- LangChain
- LangGraph
- OpenAI API / Groq API
- Tavily Search API
- BeautifulSoup
- Requests
- Streamlit
- Python-dotenv

---

## 📂 Project Structure

```
Multi-Agent-System/
│
├── app.py                 # Streamlit UI
├── pipeline.py            # Main research workflow
├── agents.py              # AI agents
├── tools.py               # Search & scraping tools
├── requirements.txt
├── .gitignore
└── README.md
```


---


## 🧩 Workflow

1. User enters a research topic.
2. Search Agent performs real-time web search.
3. Reader Agent scrapes relevant webpages.
4. Writer Agent generates a structured report.
5. Critic Agent evaluates report quality.
6. Final report is displayed in Streamlit.

---

## 📦 Future Improvements

- PDF export
- Citation generation
- Multi-source summarization
- Memory support
- RAG integration
- Multi-agent collaboration
- Chat history
- Async execution
- Streaming responses

---

## 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository and submit a pull request.


---



## 👨‍💻 Author

**Amit Kumar Singh**

GitHub:
https://github.com/amitsingh088

LinkedIn:
https://www.linkedin.com/in/amit-kumar-singh-983947288/

---
