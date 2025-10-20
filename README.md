# AI Guardrail Framework

A framework that leverages AWS Bedrock and formal methods to automatically detect unsafe or private data in model outputs.

## Current Features

### AWS Bedrock Model Tester Web App

A web application that allows you to:
- Select from multiple AI models available through AWS Bedrock
- Submit custom prompts to any selected model
- View model responses with token usage statistics
- Test models including Claude 3.5, Llama 3.1, Mistral, and Amazon Titan

## Setup

### Prerequisites

- Python 3.8+
- AWS Bedrock API access with a bearer token
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-guardrail-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your AWS Bedrock credentials in `.env`:
```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bearer-token-here
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

3. Select a model from the dropdown menu
4. Enter your prompt in the text box
5. Click "Submit Prompt" to get a response

## Available Models

The application supports the following AWS Bedrock models:

- **Anthropic**: Claude 3.5 Sonnet v2, Claude 3.5 Haiku, Claude 3 Sonnet, Claude 3 Haiku
- **Amazon**: Titan Text Express, Titan Text Lite
- **Meta**: Llama 3.1 70B Instruct, Llama 3.1 8B Instruct
- **Mistral AI**: Mistral Large, Mistral 7B Instruct

## API Endpoints

### `GET /api/models`
Returns a list of available models.

**Response:**
```json
{
  "models": [
    {
      "id": "model-id",
      "name": "Model Name",
      "provider": "Provider Name"
    }
  ]
}
```

### `POST /api/invoke`
Invokes a Bedrock model with the provided prompt.

**Request:**
```json
{
  "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
  "prompt": "Your prompt here"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Model response text",
  "model_id": "model-id",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 50,
    "total_tokens": 60
  }
}
```

## Project Structure

```
ai-guardrail-framework/
├── app.py              # Flask backend server
├── static/
│   └── index.html      # Frontend web interface
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not committed)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Future Development

This project will expand to include:
- Guardrail detection mechanisms
- Formal verification of safety properties
- Privacy-preserving analysis
- Custom rule definition system
- Real-time output filtering

## License

See LICENSE file for details.
