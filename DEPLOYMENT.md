# LangGraph Platform Deployment Guide

This guide explains how to deploy your React Agent to the LangGraph platform with environment variables managed through the UI.

## Prerequisites

1. A LangGraph platform account
2. API keys for the services you plan to use:
   - **Tavily API Key** (required for search functionality)
   - **Anthropic API Key** (if using Anthropic models - this is the default)
   - **OpenAI API Key** (if using OpenAI models)

## Configuration

The `langgraph.json` file has been configured with the following environment variables:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/react_agent/graph.py:graph"
  },
  "env": ".env",
  "environment_variables": [
    "TAVILY_API_KEY",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY"
  ]
}
```

## Deployment Steps

### 1. Deploy to LangGraph Platform

1. Push your code to your Git repository
2. In the LangGraph platform UI:
   - Create a new application
   - Connect your Git repository
   - Select the branch you want to deploy
   - The platform will automatically detect your `langgraph.json` configuration

### 2. Configure Environment Variables in UI

Once deployed, you'll need to set up your environment variables in the LangGraph platform UI:

1. Navigate to your application's **Settings** or **Environment Variables** section
2. Add the required environment variables:

   - **TAVILY_API_KEY**: Your Tavily search API key

     - Get it from: https://app.tavily.com/sign-in
     - Required for the search tool functionality

   - **ANTHROPIC_API_KEY**: Your Anthropic API key (if using Claude models)

     - Get it from: https://console.anthropic.com/
     - Required for default model: `anthropic/claude-3-5-sonnet-20240620`

   - **OPENAI_API_KEY**: Your OpenAI API key (if using OpenAI models)
     - Get it from: https://platform.openai.com/api-keys
     - Required for models like: `openai/gpt-4`, `openai/gpt-3.5-turbo`, etc.

### 3. Model Configuration

The application supports configurable models through the UI. You can:

1. Use the default: `anthropic/claude-3-5-sonnet-20240620`
2. Or configure any supported model in the format: `provider/model-name`

Supported providers include:

- `anthropic/` - Requires `ANTHROPIC_API_KEY`
- `openai/` - Requires `OPENAI_API_KEY`

### 4. Testing the Deployment

After setting up environment variables:

1. The platform will automatically restart your application
2. Test the agent by sending queries that require search functionality
3. Verify that the correct model provider is being used
4. Check logs for any environment variable or API key issues

## Environment Variable Priority

When deployed on LangGraph platform:

1. **Platform UI Variables** - Take priority (what you set in the UI)
2. **Local .env file** - Used for local development only
3. **Default configuration** - Falls back to configuration defaults

This ensures that your production environment uses the variables you configure in the LangGraph platform UI, while local development can still use your `.env` file.

## Troubleshooting

### Missing API Keys

- Check that all required environment variables are set in the platform UI
- Verify API keys are valid and have the necessary permissions
- Look for error messages in the application logs

### Model Configuration Issues

- Ensure the model name format is correct: `provider/model-name`
- Verify you have the correct API key for your chosen provider
- Check model availability and permissions

### Search Functionality Not Working

- Verify `TAVILY_API_KEY` is properly set
- Check Tavily API key permissions and rate limits
- Review search tool configuration in `src/react_agent/tools.py`
