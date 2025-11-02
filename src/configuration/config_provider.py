import os
from dotenv import load_dotenv
from loguru import logger
from pydantic import ValidationError
from tomllib import load, TOMLDecodeError
from src.configuration.config_models import ProfileConfig, WorkerConfig

class ConfigurationProvider:
    def __init__(self, ):
        self._profile_config: ProfileConfig = None
        self._worker_config: WorkerConfig = None

    @property
    def profile_config(self) -> ProfileConfig:
        return self._profile_config

    @property
    def worker_config(self) -> WorkerConfig:
        return self._worker_config

    def load_configuration(self, profile_path: str):
        load_dotenv()
        self._profile_config = self._load_profile_config(profile_path)
        self._worker_config = self._load_worker_config()

    def _load_profile_config(self, profile_path: str) -> ProfileConfig:
        logger.info(f"Loading profile from {profile_path}...")
        try:
            with open(profile_path, "rb") as f:
                config = load(f)
            result = ProfileConfig.model_validate(config)
            logger.info(f"Successfully loaded profile: {result.name}.")
            return result
        except FileNotFoundError as e:
            logger.error("Supplied profile file does not exist at path.")
            raise e
        except TOMLDecodeError as e:
            logger.error("Supplied profile file contains invalid TOML.")
            raise e
        except ValidationError as e:
            logger.error("Supplied profile file could not be mapped to Profile model.")
            raise e

    def _load_worker_config(self) -> WorkerConfig:
        logger.info("Loading worker configuration...")
        try:
            max_workers = int(os.getenv("WORKERS_MAX_COUNT", 0))
            if max_workers <= 0:
                raise ValueError("Environment variable WORKERS_MAX_COUNT must be supplied as a value greater than 0.")
            logger.info(f"Successfully loaded worker configuration.")
            return WorkerConfig(
                max_workers=max_workers
            )
        except ValueError as e:
            logger.error("Missing or malformed environment variable when loading worker configuration.")
            raise e