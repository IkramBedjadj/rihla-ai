# Rihla AI 🇩🇿

## AI-Powered Travel Assistant for Algeria

Rihla AI is a multi-agent conversational travel assistant designed specifically for Algeria.

It helps users discover Algerian destinations, access tourism-related information, obtain real-time information through specialized tools, and build personalized travel itineraries.

The project focuses on making Algerian tourism more accessible while highlighting local heritage and under-represented destinations.

---

## 🎯 Project Objective

Rihla AI aims to provide tourists with an intelligent and personalized way to discover Algeria.

Instead of searching across multiple sources, users can interact with the assistant naturally and ask questions such as:

- What are the best places to visit in Béjaïa?
- What is the current weather in Oran?
- What can I visit in Ghardaïa?
- Plan a 3-day trip to Béjaïa.
- What are some less-known destinations in Algeria?

The system interprets the user's request and can use specialized tools to retrieve relevant information.

---

## 🧠 Multi-Agent Architecture

Rihla AI is built around a multi-agent architecture where AI agents can collaborate with specialized tools.

### Main Architecture

```text
                    User
                      │
                      ▼
              Conversational AI
                      │
                      ▼
                Rihla Agent
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Search Tool  Weather Tool  Other Tools
          │           │           │
          └───────────┼───────────┘
                      ▼
              Personalized Answer
                      │
                      ▼
                    User
```

The architecture is modular, allowing additional tourism tools and data sources to be integrated in future versions.

---

## 🛠️ Main Features

### Tourism Search

The assistant can search for tourism-related information and destinations.

### Weather Information

The system can retrieve current weather information for Algerian cities using a weather API.

### Personalized Travel Planning

The planner can generate travel itineraries according to:

- Destination
- Trip duration
- User interests
- Activities
- Tourism preferences

### Algerian Tourism Focus

The project is designed specifically for Algeria and aims to promote:

- Natural heritage
- Cultural heritage
- Historical sites
- Local destinations
- Under-represented tourism areas

### Arabic and French Support

Rihla AI is designed to interact with users in Arabic and French, making the system more accessible to Algerian users and visitors.

---

## 🌍 Tested Destinations

The prototype has been tested with real Algerian destinations, including:

- Béjaïa
- Ghardaïa
- Ouargla

The architecture is designed to progressively support all **58 wilayas of Algeria**.

---

## 💻 Technology Stack

The current prototype uses technologies including:

- Python
- Flask
- Ollama
- Local LLMs
- Requests
- Tavily
- OpenWeather API
- HTML
- CSS
- JavaScript

---

## 🤖 Local AI Model

One of the main characteristics of the current prototype is the use of a **local, self-hosted AI model through Ollama**.

This approach allows the project to operate without depending entirely on paid AI model APIs.

### Advantages

Using a local model provides:

- Lower infrastructure costs during the prototype stage
- Greater control over the AI environment
- No mandatory paid LLM API for the core model
- The ability to experiment and develop locally

### Current Limitations

Because the prototype uses a local and relatively lightweight model running on local hardware, its performance is not equivalent to larger commercial cloud-based models.

As a result:

- Response times can sometimes be slower.
- Complex requests may require more processing time.
- The quality and depth of some generated responses may be lower than those produced by larger models.
- Performance depends on the hardware running the local model.

These limitations are related to the current prototype environment and do not represent limitations of the overall Rihla AI architecture.

With access to stronger models and appropriate infrastructure, future versions could improve:

- Response speed
- Reasoning capabilities
- Recommendation quality
- Information processing
- Overall user experience

---

## 🔎 Information Sources and Tools

Rihla AI can combine AI reasoning with external tools and information sources.

The current architecture includes tools for tasks such as:

- Tourism search
- Weather retrieval
- Local information discovery

The system is designed to progressively integrate additional reliable tourism data sources.

For production deployment, information validation and source reliability will be further strengthened.

---

## 🚀 Scalability Roadmap

### Current Stage

- Functional prototype
- Multi-agent architecture
- Tourism search
- Weather integration
- Testing on Béjaïa, Ghardaïa, and Ouargla

### Next Steps

- Expand coverage to all 58 wilayas
- Add more tourism data sources
- Improve recommendation quality
- Improve response speed
- Develop a public web platform
- Add voice interaction
- Integrate additional tourism-sector services

---

## 🏆 IA Tour Algérie 2026

Rihla AI is submitted to:

**IA Tour Algérie 2026**

### Strategic Axis

**Axe 02 — Sur-Mesure**

The project aligns with the competition's focus on:

- Conversational AI
- Personalized tourism experiences
- Intelligent recommendations

---

## 📌 Proof of Concept

Rihla AI has a functional prototype that demonstrates the application of conversational AI to Algerian tourism.

The prototype has been tested using real destinations and tourism-related requests.

The current implementation demonstrates the technical feasibility of the concept while leaving room for further improvements in model performance, data coverage, and infrastructure.

---

## 🔐 Security & Responsible AI

The project aims to follow responsible AI principles, including:

- Protecting API keys and credentials
- Avoiding unnecessary personal-data collection
- Using reliable information sources where possible
- Reducing potential recommendation biases
- Maintaining regional and cultural neutrality

Sensitive credentials such as API keys should never be committed to the repository.

---

## 📂 Project Structure

```text
rihla-ai/
│
├── app.py
├── search_agent.py
├── run_agent.py
├── tools.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── .gitignore
```

The exact structure may evolve as the project develops.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rihla-ai.git
cd rihla-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and add the required API keys.

Example:

```env
TAVILY_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
```

Do not commit the `.env` file to GitHub.

### 6. Run the application

```bash
python app.py
```

The application will normally be available locally at:

```text
http://127.0.0.1:5000
```

---

## 🔮 Future Vision

The long-term vision of Rihla AI is to become an AI-powered travel companion for Algeria.

The project aims to evolve toward:

**Discover → Plan → Explore → Adapt**

with national destination coverage, stronger AI models, real-time tourism information, voice interaction, and integration with the Algerian tourism ecosystem.

---

## 👩‍💻 Project

**Rihla AI**

Developed for the **IA Tour Algérie 2026** competition.

**Axe 02 — Sur-Mesure**

> Discover Algeria, Your Way. 🇩🇿
