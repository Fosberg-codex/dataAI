# Data AI

Data AI is a Python-based tool that enables natural language interactions with your datasets using various Language Learning Models (LLMs). Ask questions about your data in plain English and get insights through popular AI services.

## Features

- Natural language querying of datasets for better understanding
- Support for multiple LLM providers:
  - OpenAI
  - Azure OpenAI Services
  - Anthropic
- Console-based interface for easy interaction
- Flexible dataset compatibility
- Ideal for data analysts, data engineers, data scientists, and machine learning engineers

## Prerequisites

- Python 3.7+
- API keys for your chosen LLM provider(s):
  - OpenAI API key
  - Azure OpenAI Services API key and endpoint
  - Anthropic API key

## Installation

1. Clone the repository
```bash
git clone https://github.com/Fosberg-codex/dataAI.git
cd dataAI
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Place your dataset in the project directory

2. Run the main script:
```bash
python main.py
```

3. Follow the console prompts to:
   - Select your LLM provider
   - Enter your provider's credentials
   - Load your dataset from the base directory
   - Start asking questions about your data

Example questions you can ask:
- "What is the average value in column X?"
- "Show me the top 5 entries sorted by Y"
- "Create a summary of the trends in this dataset"
- "What are the correlations between column A and B?"

## Project Structure

```
dataAI/
├── main.py
├── config/
│   └── config.yaml
├── src/
│   ├── init.py
│   ├── data_loader.py
│   ├── config_manager.py
│   ├── api_client.py
│   ├── query_engine.py
│   └── response_generator.py
├── utils/   (optional)
│   ├── init.py
│   └── helpers.py

```

## Configuration

To switch between different LLM providers, rerun your code to select your provider of choice.

```python
# Example configuration
llm_provider = "openai"  # or "azure" or "anthropic"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Thanks to OpenAI, Azure, and Anthropic for providing the LLM services, though you still need an API key
- You may reach out to contribute
