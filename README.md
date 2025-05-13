# Healthy Toronto Agent

Find healthy and affordable food in Toronto - no cooking required.

## Project Structure
```
healthy-toronto-agent/
├── ingest.py           # Create vector DB from CSV
├── agent.py            # Q&A agent using LangChain RAG
├── data/
│   └── healthy_toronto_eat.csv  # Dataset
├── db/                 # Chroma vector DB (not in git)
├── README.md           # This file
└── requirements.txt    # Required packages
```

## Setup

1. Install requirements:
```
pip install -r requirements.txt
```

2. Add your OpenAI API key to a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## Usage

1. Create vector database (once):
```
python ingest.py
```

2. Run the agent:
```
python agent.py
```

3. Ask questions about healthy restaurants in Toronto.

## Inspiration

Inspired by **Aurora Li** and **Cole Bowden** at AI Meetup Toronto by **AICamp** (May 2025).

---

🗂️ Dataset constructed manually using publicly available restaurant information (e.g., address, category, dietary options). No copyrighted content used.  
If you believe any information should not be included, please open an issue and it will be promptly reviewed or removed.