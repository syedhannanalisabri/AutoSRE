# AutoSRE: A Self-Healing DevOps System 🤖⚕️
### Built with PydanticAI & Docker

**AutoSRE** is a proof-of-concept autonomous agent that monitors server health and performs self-healing actions without human intervention. Monitoring a "broken" Docker container, the agent detects memory leaks and automatically restarts the service to restore system stability.

## 🚀 Features
- **Autonomous Monitoring**: Continuously checks container stats (CPU/Memory) and logs.
- **Self-Healing**: Automatically detects memory spikes (>50MB) or error logs and restarts the container.
- **LLM-Powered Reasoning**: Uses **Google Gemini 1.5 Flash** (via PydanticAI) to make decisions based on system state.
- **Docker Integration**: Direct interaction with the Docker SDK for real-time control.

## 🛠️ Tech Stack
- **AI/Agent**: Python 3.11, PydanticAI, Google Gemini Flash
- **Infrastructure**: Docker SDK for Python
- **Application**: Flask (Victim App)
- **Observability**: Logfire (Optional)

## 📦 quickstart

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/AutoSRE.git
cd AutoSRE
pip install -r requirements.txt
```

### 2. Configure Keys
Create a `.env` file in the root:
```env
GEMINI_API_KEY=your_google_api_key
```

### 3. Run the System
```bash
# 1. Build & Run the Victim App (The "Broken" Server)
docker build -t victim_app ./victim_app
docker run -d --name production-server -p 5000:5000 victim_app

# 2. Start the AutoSRE Agent
python -m agent.main
```

### 4. Simulate a Crash
Trigger a memory leak to test the agent:
```bash
curl http://localhost:5000/leak
```
Watch the agent console—it will detect the spike and restart the container automatically!

## 📜 License
MIT
