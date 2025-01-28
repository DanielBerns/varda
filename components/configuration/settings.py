import os

from pathlib import Path
from typing import Dict, Tuple, Callable

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from components.helpers import get_directory

class Settings:
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

    def __init__(
        self,
        identifier: str, 
        major: int,
        minor: int,
        patch: int,
        mode: str, 
        dotenv: str
    ) -> None:
        self._user_home = Path("~").expanduser()
        self._semantic_version = f"{major:d}.{minor:d}.{patch:d}"

        # where the settings file, database, results and reports live        
        self._info_home = get_directory(
            Path(self.user_home, "Info", identifier, semantic_version, mode)
        )
        # where the code lives        
        self._software_home = get_directory(
            Path(self.user_home, "Software", identifier, semantic_version)
        )
        # where cli commands for automation live        
        self._commands_home = get_directory(
            Path(self.user_home, "Commands", identifier, semantic_version)
        )
        # where secrets live        
        self._secrets_home = get_directory(
            Path(self.user_home, "Secrets", identifier, semantic_version)
        )        

        self._log_level_key: str = f"{identifier.upper():s}_LOG_LEVEL"        
        resource = Path(info_home).with_name(dotenv)
        Settings.read_dotenv(
            resource, 
            {"log_level_key": self.log_level_key, "log_level": "DEBUG"}
        )
        self._log_level: str = os.environ.get(self.log_level_key) or "DEBUG"

    @property
    def user_home(self) -> Path:
        return self._user_home
    
    @property
    def semantic_version(self) -> str:
        return self._semantic_version
    
    @property
    def info_home(self) -> Path:
        return self._info_home
    
    @property
    def software_home(self) -> Path:
        return self._software_home
    
    @property
    def commands_home(self) -> Path:
        return self._commands_home

    @property
    def secrets_home(self) -> Path:
        return self._secrets_home

    @property
    def log_level_key(self) -> str:
        return self._log_level_key
    
    @property
    def log_level(self) -> str:
        return self._log_level
    
