# src/config_manager.py
from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import yaml
from getpass import getpass
import json
from pathlib import Path

@dataclass
class APIConfig:
    provider: str
    api_key: str
    azure_endpoint: Optional[str] = None
    deployment_name: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ConfigManager:
    def __init__(self, config_file: str = "config/config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self.api_config: Optional[APIConfig] = None

    def _load_config(self) -> dict:
        """Load configuration from file or create default if not exists"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            default_config = {
                "api": {
                    "default_provider": "openai",
                    "openai": {
                        "model": "gpt-4",
                        "temperature": 0.7,
                        "max_tokens": 2000
                    },
                    "azure": {
                        "model_deployment": "",
                        "api_version": "2024-02-15-preview",
                        "temperature": 0.7,
                        "max_tokens": 2000
                    },
                    "anthropic": {
                        "model": "claude-3-opus-20240229",
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                },
                "data": {
                    "max_rows": 5000,
                    "sample_size": 5
                },
                "system": {
                    "debug": False,
                    "log_level": "INFO"
                }
            }
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            return default_config

    def _save_config(self) -> None:
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def setup_api_configuration(self) -> APIConfig:
        """Setup API configuration based on user input"""
        print("\n=== API Configuration Setup ===")
        print("1. OpenAI API")
        print("2. Azure OpenAI API")
        print("3. Anthropic Claude API")
        
        while True:
            choice = input("\nSelect API provider (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("Invalid choice. Please select 1, 2, or 3.")

        if choice == '1':
            api_key = self._get_api_key('OPENAI_API_KEY', 'OpenAI')
            config = self.config['api']['openai']
            self.api_config = APIConfig(
                provider='openai',
                api_key=api_key,
                model=config['model'],
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
        elif choice == '2':
            api_key = self._get_api_key('AZURE_OPENAI_API_KEY', 'Azure OpenAI')
            endpoint = self._get_azure_endpoint()
            deployment = self._get_azure_deployment()
            config = self.config['api']['azure']
            self.api_config = APIConfig(
                provider='azure',
                api_key=api_key,
                azure_endpoint=endpoint,
                deployment_name=deployment,
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
        else:
            api_key = self._get_api_key('ANTHROPIC_API_KEY', 'Anthropic')
            config = self.config['api']['anthropic']
            self.api_config = APIConfig(
                provider='anthropic',
                api_key=api_key,
                model=config['model'],
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )

        # Update config with new provider
        self.config['api']['default_provider'] = self.api_config.provider
        
        # For Azure, update the deployment name
        if self.api_config.provider == 'azure':
            self.config['api']['azure']['model_deployment'] = self.api_config.deployment_name
        
        # Save the updated configuration
        self._save_config()
        
        return self.api_config

    def _get_api_key(self, env_var: str, service_name: str) -> str:
        """Get API key from environment variable or user input"""
        api_key = os.getenv(env_var)
        if api_key:
            use_env = input(f"\nFound {service_name} API key in environment variables. Use this? (y/n): ")
            if use_env.lower() == 'y':
                return api_key

        while True:
            api_key = getpass(f"\nEnter your {service_name} API key: ")
            if api_key.strip():
                return api_key
            print("API key cannot be empty.")

    def _get_azure_endpoint(self) -> str:
        """Get Azure endpoint from environment variable or user input"""
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        if endpoint:
            use_env = input("\nFound Azure endpoint in environment variables. Use this? (y/n): ")
            if use_env.lower() == 'y':
                return endpoint

        while True:
            endpoint = input("\nEnter your Azure OpenAI endpoint URL: ").strip()
            if endpoint and endpoint.startswith(('http://', 'https://')):
                return endpoint
            print("Please enter a valid HTTP/HTTPS URL.")

    def _get_azure_deployment(self) -> str:
        """Get Azure deployment name from environment variable or user input"""
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        if deployment:
            use_env = input("\nFound Azure deployment name in environment variables. Use this? (y/n): ")
            if use_env.lower() == 'y':
                return deployment

        while True:
            deployment = input("\nEnter your Azure OpenAI deployment name: ").strip()
            if deployment:
                return deployment
            print("Deployment name cannot be empty.")

    def get_data_config(self) -> Dict[str, Any]:
        """Get data processing configuration"""
        return self.config.get('data', {})

    def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration"""
        return self.config.get('system', {})