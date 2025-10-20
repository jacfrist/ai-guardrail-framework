import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize AWS Bedrock client
def get_bedrock_client():
    """Create and return a Bedrock Runtime client with bearer token authentication."""
    # Get the bearer token from environment
    bearer_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')

    if not bearer_token:
        raise ValueError('AWS_BEARER_TOKEN_BEDROCK environment variable is not set')

    # Ensure the environment variable is set for boto3
    os.environ['AWS_BEARER_TOKEN_BEDROCK'] = bearer_token

    # According to AWS docs, boto3 automatically uses the bearer token from environment
    # when AWS_BEARER_TOKEN_BEDROCK is set
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'
    )

    return client

# Common AWS Bedrock models
AVAILABLE_MODELS = [
    {
        'id': 'us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        'name': 'Claude 3.5 Sonnet v2',
        'provider': 'Anthropic'
    },
    {
        'id': 'us.anthropic.claude-3-5-haiku-20241022-v1:0',
        'name': 'Claude 3.5 Haiku',
        'provider': 'Anthropic'
    },
    {
        'id': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'name': 'Claude 3 Sonnet',
        'provider': 'Anthropic'
    },
    {
        'id': 'anthropic.claude-3-haiku-20240307-v1:0',
        'name': 'Claude 3 Haiku',
        'provider': 'Anthropic'
    },
    {
        'id': 'amazon.titan-text-express-v1',
        'name': 'Titan Text Express',
        'provider': 'Amazon'
    },
    {
        'id': 'amazon.titan-text-lite-v1',
        'name': 'Titan Text Lite',
        'provider': 'Amazon'
    },
    {
        'id': 'meta.llama3-1-70b-instruct-v1:0',
        'name': 'Llama 3.1 70B Instruct',
        'provider': 'Meta'
    },
    {
        'id': 'meta.llama3-1-8b-instruct-v1:0',
        'name': 'Llama 3.1 8B Instruct',
        'provider': 'Meta'
    },
    {
        'id': 'mistral.mistral-large-2402-v1:0',
        'name': 'Mistral Large',
        'provider': 'Mistral AI'
    },
    {
        'id': 'mistral.mistral-7b-instruct-v0:2',
        'name': 'Mistral 7B Instruct',
        'provider': 'Mistral AI'
    },
    {
        'id': 'openai.gpt-oss-120b-1:0',
        'name': 'GPT-OSS 120B',
        'provider': 'OpenAI'
    },
    {
        'id': 'openai.gpt-oss-20b-1:0',
        'name': 'GPT-OSS 20B',
        'provider': 'OpenAI'
    },
    {
        'id': 'deepseek.r1-v1:0',
        'name': 'DeepSeek R1',
        'provider': 'DeepSeek'
    },
    {
        'id': 'deepseek.v3-v1:0',
        'name': 'DeepSeek V3.1',
        'provider': 'DeepSeek'
    }
]

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('static', 'index.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Return the list of available models."""
    return jsonify({'models': AVAILABLE_MODELS})

@app.route('/api/invoke', methods=['POST'])
def invoke_model():
    """Invoke a Bedrock model with the provided prompt."""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        prompt = data.get('prompt')

        if not model_id or not prompt:
            return jsonify({'error': 'model_id and prompt are required'}), 400

        # Create Bedrock client
        client = get_bedrock_client()

        # Use the Converse API for unified interface across models
        messages = [
            {
                'role': 'user',
                'content': [{'text': prompt}]
            }
        ]

        # Configure inference parameters
        inference_config = {
            'maxTokens': 2048,
            'temperature': 0.7,
            'topP': 0.9
        }

        # Invoke the model
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config
        )

        # Extract the response text
        output_message = response['output']['message']
        response_text = output_message['content'][0]['text']

        # Get usage metrics
        usage = response.get('usage', {})

        return jsonify({
            'success': True,
            'response': response_text,
            'model_id': model_id,
            'usage': {
                'input_tokens': usage.get('inputTokens', 0),
                'output_tokens': usage.get('outputTokens', 0),
                'total_tokens': usage.get('totalTokens', 0)
            }
        })

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return jsonify({
            'success': False,
            'error': f'AWS Bedrock Error ({error_code}): {error_message}'
        }), 500

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error invoking model: {error_details}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Check if AWS bearer token is set
    if not os.getenv('AWS_BEARER_TOKEN_BEDROCK'):
        print('WARNING: AWS_BEARER_TOKEN_BEDROCK environment variable is not set!')
        print('Please set it in your .env file')

    print('Starting Flask server on http://localhost:5001')
    app.run(debug=True, host='0.0.0.0', port=5001)
