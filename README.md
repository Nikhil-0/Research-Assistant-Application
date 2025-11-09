# Research Assistant Application

A powerful research assistant that uses AI to help gather, synthesize, and evaluate information on any topic. Built with Streamlit and ADK (AI Development Kit).

## Features

- Multi-agent system with specialized roles:
  - Research Agent: Gathers information from various sources
  - Synthesis Agent: Organizes and structures information
  - Evaluation Agent: Validates and ensures quality
- Real-time chat interface
- Session management
- Progress tracking
- Error handling
- Flexible output formatting:
  - Multiple format options (report, debate, meta-analysis, point form, essay)
  - Adjustable length and complexity
  - Option to expand or refine research with follow-up prompts

## Prerequisites

- Python 3.12 or higher
- ADK (AI Development Kit)
- Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Nikhil-0/Research-Assistant-Application.git
cd Research-Assistant-Application
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the ADK server:
```bash
adk web
```

2. In another terminal, run the Streamlit app:
```bash
streamlit run app/ResearchApp.py
```

3. Open your browser and navigate to the URL shown by Streamlit (usually http://localhost:8501)

## Project Structure

- `app/ResearchApp.py`: Main Streamlit application
- `multi_tool_agent/`: Contains the agent implementation
  - `agent.py`: Defines the multi-agent system
  - `__init__.py`: Package initialization

## Future Improvements

1. Add support for different output formats:
   - Debate style
   - Formal report
   - Meta-analysis
   - Point-form summary
   - Essay format
2. Implement length and complexity controls
3. Add features for expanding or editing existing research
4. Enhance source citation and verification

## License

MIT License

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request
