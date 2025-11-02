import argparse
import inject

from loguru import logger
from src.configuration import ConfigurationProvider

parser = argparse.ArgumentParser(description="Web Crawler")
parser.add_argument("--profile", type=str, required=True, help="Path to the profile toml file")
args = parser.parse_args()

def main():
    logger.info("Starting Web Crawler...")
    configuration_provider = ConfigurationProvider()
    configuration_provider.load_configuration(args.profile)

    def configure_dependencies(binder: inject.Binder):
        binder.bind(ConfigurationProvider, configuration_provider)

    inject.configure(configure_dependencies)
