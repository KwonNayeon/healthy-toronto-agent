# Development Log

## Project Context
Added a web frontend to my existing console-based LangChain RAG chatbot using Streamlit. The core chatbot logic was already built and working locally - this was about creating a user-friendly web interface.

## Key Challenges & Solutions

### First Encounter with Dependency Management
**Background**: This was my first experience managing complex ML package dependencies.
**Issue**: Installing requirements.txt failed due to LangChain ecosystem changes.
```
ERROR: Cannot install -r requirements.txt because these package versions have conflicting dependencies.
```
**Root Cause**: LangChain split into multiple packages (`langchain-core`, `langchain-community`, `langchain-openai`) but my requirements.txt used old unified package structure.
**Solution**: 
- Installed `langchain-community` separately for Chroma integration
- Used flexible version ranges instead of exact pinning
**Learning**: Package ecosystems evolve rapidly in ML/AI space. Version management is crucial for reproducible environments.

### Data Limitations Revealed Through User Testing
**Issue**: Chat responses like "specific nutritional information for each dish is not provided in the context given"
**Root Cause**: Current database schema only includes basic fields:
```
name, address, category, price_range, vegan, vegetarian, gluten_free, grab_and_go, open_status, notes
```
**Impact**: Limits chatbot's ability to answer detailed nutrition-focused queries that users naturally ask.
**Future Enhancement**: Need to expand dataset with nutritional details, specific menu items, and detailed ingredient information to make the chatbot truly useful for health-conscious users.

## Key Learnings
1. **Dependency Management**: Complex ML packages require careful version coordination
2. **Data-Driven Limitations**: RAG systems are only as good as their underlying data quality and completeness
3. **User Testing Value**: Real user interactions reveal data gaps not apparent during development