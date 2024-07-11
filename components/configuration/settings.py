import os

from pathlib import Path
from typing import Dict, Tuple, Callable

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from components.helpers import get_directory

HOME = Path("~").expanduser()

class Settings:
    # where the settings file, database, results and reports live
    INFO: Path = Path(HOME, "Info").expanduser()
    # where the code lives
    SOFTWARE: Path = Path(HOME, "Software").expanduser()
    # where cli commands for automation live
    COMMANDS: Path = Path(HOME, "Commands").expanduser()    
    
    @staticmethod
    def semantic_version(
        major: int, 
        minor: int, 
        patch: int
    ) -> str:
        return f"{major:d}.{minor:d}.{patch:d}"
    
    @staticmethod
    def write_dotenv(
        resource: Path, 
        expected: Dict[str, str]
    ) -> None:
        """Write an example dotenv file, with expected keys and values.
        User may modify the values, and add explanations.
        See https://pypi.org/project/python-dotenv/
        """
        with open(resource, "w") as target:
            target.write("# settings\n")
            for key, value in expected.items():
                target.write(f"{key:s}={value:s}\n")

    @staticmethod
    def read_dotenv(
        resource: Path,
        default_content: Dict[str, str]
    ) -> None:
        """Load key value pairs from a text file
        and set some environment variables.
        If resource doesn't exists,
           create it with default content
        """
        if not resource.exists():
            Settings.write_dotenv(resource, default_content)
        load_dotenv(resource)

    @staticmethod
    def build(
        identifier: str, 
        major: int,
        minor: int,
        patch: int,
        mode: str, 
        dotenv: str
    ) -> Dict[str, str]:
        semantic_version = Settings.semantic_version(major, minor, patch)
        info_home = get_directory(
            Path(Settings.INFO, identifier, semantic_version, mode)
        )
        software_home = get_directory(
            Path(Settings.SOFTWARE, identifier, semantic_version)
        )
        commands_home = get_directory(
            Path(Settings.COMMANDS, identifier, semantic_version)
        )
        resource = Path(info_home, identifier).with_name(dotenv)
        Settings.read_dotenv(resource, {})
        
        log_level_key: str = f"{identifier.upper():s}_LOG_LEVEL"
        log_level: str = os.environ.get(log_level_key) or "DEBUG"

        return {
            "mode": mode,
            "semantic_version": semantic_version,
            "identifier": identifier,
            "info_home": str(info_home),
            "software_home": str(software_home),
            "commands_home": str(commands_home),            
            "log_level_key": log_level_key,
            log_level_key: log_level,
        }
