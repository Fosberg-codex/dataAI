# src/api_client.py
from typing import Dict, Any
import openai
from openai import OpenAI
from openai import AzureOpenAI
import anthropic
from src.config_manager import APIConfig

class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.7):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def analyze(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analysis assistant. Provide clear, concise, and accurate analysis of the data presented."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

class AzureOpenAIClient:
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, temperature: float = 0.7):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )
        self.deployment_name = deployment_name
        self.temperature = temperature

    def analyze(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a data analysis assistant. Provide clear, concise, and accurate analysis of the data presented."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Azure OpenAI API error: {str(e)}")

class AnthropicClient:
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229", temperature: float = 0.7):
        self.client = anthropic.Client(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def analyze(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=self.temperature,
                system="You are a data analysis assistant. Provide clear, concise, and accurate analysis of the data presented.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

class APIClientFactory:
    @staticmethod
    def create_client(config: APIConfig):
        if config.provider == 'openai':
            return OpenAIClient(
                api_key=config.api_key,
                model=config.model,
                temperature=config.temperature
            )
        elif config.provider == 'azure':
            return AzureOpenAIClient(
                api_key=config.api_key,
                endpoint=config.azure_endpoint,
                deployment_name=config.deployment_name,
                temperature=config.temperature
            )
        elif config.provider == 'anthropic':
            return AnthropicClient(
                api_key=config.api_key,
                model=config.model,
                temperature=config.temperature
            )
        else:
            raise ValueError(f"Unsupported API provider: {config.provider}")