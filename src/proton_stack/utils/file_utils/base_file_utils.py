"""
utils/file_utils/base_file_utils.py
-----------------------------------

The following file contains the BaseFileUtils implementation 
to be inherited by the other modality-based classes.
"""
import json

# Note: abstractmethod operates on a class instance while
# abstractclassmethod operates on the class itself.
#   - abstractmethod calls instance.method()
#   - abstractclassmethod calls class.method()
from abc import abstractmethod
from typing import Any, Dict, List
from pathlib import Path


class BaseFileUtils:
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    # ============================================================================
    # Common utils
    # ============================================================================
    @abstractmethod
    def read_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def save_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def supported_backends(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def supported_formats(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def read_metadata(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def write_metadata(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def verify_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def read_bytes(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def save_bytes(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def convert_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def get_checksum(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def create_dir(
        self,
        path: Path,
    ) -> None:
        """
        Creates a directory from a given path.
        Could be both a file path or a directory path.
        For file paths, it creates the parent directory.

        Args:
            path (Path): The file path or folder path from which \
                the directories need to be created.
        """
        path.mkdir(parents=True, exist_ok=True)
        
    def validate_file_path(
        self,
        path: Path,        
    ) -> None:
        """
        Checks if a file path is an actual file path, it exists, 
        and is greater than 0 bytes.

        Args:
            path (Path): The file path to validate.
        """
        if not path.is_file():  # Checks if the path corresponds to a file
            raise RuntimeError(
                f"The file with path: {str(path)} is not an actual file."
            )
        if not path.exists():  # Checks if the file exists
            raise FileNotFoundError(
                f"The file with path: {str(path)} does not exist."
            )
        if not path.stat().st_size > 0:  # checks if the file is not 0 bytes
            raise RuntimeError(
                f"The file with path: {str(path)} is corrupted as its size if 0 bytes."
            )
    
    def validate_dir_path(
        self,
        path: Path,
    ) -> None:
        """
        Checks if a directory path is a directory and if it exists.

        Args:
            path (Path): The directory path to check.
        """
        if not path.is_dir():  # Checks if the path corresponds to a directory
            raise RuntimeError(
                f"The provided folder path: {str(path)} is not a dir path."
            )
        if not path.exists():  # Checks if the path exists or not
            raise RuntimeError(
                f"The provided folder path: {str(path)} doesn't exists."
            )
    
    def validate_format(
        self,
        path: Path,
        supported_formats: List[str],
    ) -> None:
        """
        Checks if the path exists in the supported formats.

        Args:
            path (Path): The path for checking file format support.
            supported_formats (List[str]): The list of supported formats for \
                a modality.
        """
        file_suffix = path.suffix.lower()
        if file_suffix not in supported_formats:
            raise RuntimeError(
                f"File with format: {file_suffix} is not supported. Supported \
                    file formats include: {supported_formats}"
            )
    
    def validate_json(
        self,
        obj: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        """
        Checks if the loaded *.json file is a valid json.

        Args:
            obj (Dict[Any, Any]): The loaded *.json object.

        Returns:
            Dict[Any, Any]: The validated *.json object.
        """
        if not isinstance(obj, dict):
            raise ValueError(
                "Object must be a JSON object."
            )
        return obj
    
    def read_json(
        self,
        path: Path,
        encoding: str = "utf-8",
    ) -> Dict[Any, Any]:
        """
        Reads a *.json file.
        
        Note: *.json doesn't support certain formats and requires explicit \
            conversion. Example as follows:
            
            ```python
                data = {
                    "created_at": datetime.now(),
                    "source": Path("data.csv"),
                }

                # Convert special types into JSON-compatible values.
                serializable = {
                    "created_at": data["created_at"].isoformat(),
                    "source": str(data["source"]),
                }
                
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(serializable, file, indent=4)

                with open("data.json", "r", encoding="utf-8") as file:
                    loaded = json.load(file)

                # Restore the desired Python types.
                loaded["created_at"] = datetime.fromisoformat(loaded["created_at"])
                loaded["source"] = Path(loaded["source"])
            ```

        Args:
            path (Path): The path to the *.json file.
            encoding (str, optional): The optional encoding type for the \
                read method. Defaults to "utf-8".

        Returns:
            Dict[Any, Any]: The loaded json file.
        """
        self.validate_file_path(path=path)
        with open(str(path), "r", encoding=encoding) as file:
            loaded = json.load(file)
        return self.validate_json(loaded)
    
    def save_json(
        self,
        obj: Dict[Any, Any],
        path: Path,
        encoding: str = "utf-8"
    ) -> None:
        """
        Saves a *.json file.
        
        Note: *.json doesn't support certain formats and requires explicit \
            conversion. Example as follows:
            
            ```python
                data = {
                    "created_at": datetime.now(),
                    "source": Path("data.csv"),
                }

                # Convert special types into JSON-compatible values.
                serializable = {
                    "created_at": data["created_at"].isoformat(),
                    "source": str(data["source"]),
                }
                
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(serializable, file, indent=4)

                with open("data.json", "r", encoding="utf-8") as file:
                    loaded = json.load(file)

                # Restore the desired Python types.
                loaded["created_at"] = datetime.fromisoformat(loaded["created_at"])
                loaded["source"] = Path(loaded["source"])
            ```
            
        Args:
            obj (Dict[Any, Any]): The object to be serialized and \
                save as a *.json.
            path (Path): The path to the *.json file.
            encoding (str, optional): The optional encoding type for the \
                write method. Defaults to "utf-8".
        """
        self.create_dir(path=path)
        with open(str(path), "w", encoding=encoding) as file:
            json.dump(obj, file, indent=4, ensure_ascii=False)
