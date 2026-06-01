from dataclasses import dataclass
from strands.models import BedrockModel,CacheConfig

@dataclass
class Settings:
    model_name: str = "us.amazon.nova-pro-v1:0"
    region_name: str = "us-east-1"
    max_tokens: int = 4096
    temperature: float = 0.7

    def get_model(self):
        return BedrockModel(model_id=self.model_name,
                            region_name=self.region_name,
                            max_tokens=self.max_tokens,
                            temperature=self.temperature,
                            cache_config=CacheConfig(strategy="auto"))

settings = Settings()