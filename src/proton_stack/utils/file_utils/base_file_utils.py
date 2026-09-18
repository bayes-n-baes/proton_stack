"""
Supports the common operations involving any random
document or file from different types of modality.
Allows to read & write files in different formats, 
fetch file metadata and save the same.
"""
import hashlib
import json

# Note: abstractmethod operates on a class instance while
# abstractclassmethod operates on the class itself.
#   - abstractmethod calls instance.method()
#   - abstractclassmethod calls class.method()
from abc import abstractmethod, ABC
from typing import Any, Dict, List
from pathlib import Path


class BaseFileUtils(ABC):
    
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base utility without allocating resources.
        """
        pass
    
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
        
    def validate_file_path(
        self,
        path: Path,        
    ) -> None:
        """
        Require a path to reference an existing, non-empty regular file.
        
        This validates filesystem properties only, not file contents or
        format integrity. Symbolic links are followed. Validation does not
        guarantee that the path remains unchanged before a later read.

        Args:
            path (Path): File path to inspect.
        """
        if not path.is_file():  # Checks if the path corresponds to a file
            raise RuntimeError(
                f"The file with path {str(path)} is not an actual file."
            )
        if not path.exists():  # Checks if the file exists
            raise FileNotFoundError(
                f"The file with path {str(path)} does not exist."
            )
        if not path.stat().st_size > 0:  # checks if the file is not 0 bytes
            raise RuntimeError(
                f"The file with path {str(path)} has 0 bytes."
            )
    
    def validate_dir_path(
        self,
        path: Path,
    ) -> None:
        """
        Require a path to reference an existing directory.
        
        Symbolic links are followed. This does not check whether the
        directory is readable or writable.

        Args:
            path (Path): Directory path to inspect.
        """
        if not path.is_dir():  # Checks if the path corresponds to a directory
            raise RuntimeError(
                f"The provided folder path {str(path)} is not a dir path."
            )
        if not path.exists():  # Checks if the path exists or not
            raise RuntimeError(
                f"The provided folder path {str(path)} doesn't exists."
            )
    
    def validate_format(
        self,
        path: Path,
        supported_formats: List[str],
    ) -> None:
        """
        Check a path's final suffix against the allowed file formats.
        
        Only the path suffix is checked; file contents are not inspected.
        Compound extensions are not combined: data.csv.gz has suffix .gz.
        The supplied list of supported formats is not normalized.

        Args:
            path (Path): Path whose suffix is checked; it need not exist.
            supported_formats (List[str]): Allowed lowercase suffixes with
                leading dots, such as [".csv", ".parquet"].
        """
        file_suffix = path.suffix.lower()
        if file_suffix not in supported_formats:
            raise RuntimeError(
                f"File with format {file_suffix} is not supported. Supported \
                    file formats include {", ".join(supported_formats)}."
            )
    
    def get_checksum(
        self,
        path: Path,
        algorithm: str = "sha256",
        chunk_size: int = 1024*1024,
    ) -> str:
        """
        Compute a hexadecimal digest of a nonempty file.
        
        chunk_size is not validated. Zero hashes no content; a negative
        value reads the remaining file into memory at once.

        Args:
            path (Path): Existing, nonempty file to hash.
            algorithm (str, optional): Algorithm name accepted by hashlib.new
                whose hexdigest method requires no length argument, such as
                "sha256", "sha512", or "md5". Defaults to "sha256".
            chunk_size (int, optional): Bytes requested per read. Use a positive
                integer to hash the complete file in bounded chunks. Defaults
                to 1,048,576 bytes (1 MiB).

        Returns:
            str: Hexadecimal digest of the bytes read from the file.
        """
        self.validate_file_path(path=path)
        hasher = hashlib.new(algorithm)
        
        # reads the file bytes and updates the hash algorithm
        with path.open("rb") as file:
            while chunk := file.read(chunk_size):
                hasher.update(chunk)
                
        return hasher.hexdigest()  # returns the hexadecimal checksum value
    
    def create_dir(
        self,
        path: Path,
        is_file: bool = True,
        exist_ok: bool = True,
    ) -> None:
        """
        Create a directory or the parent directories of a destination file.
        
        Missing ancestors are created recursively. File mode does not create 
        or validate the destination file.

        Args:
            path (Path): File or directory path.
            is_file (bool, optional): If True, create only path.parent.
                If False, create path itself as a directory. Defaults to True
                for compatibility with file-writing methods.
            exist_ok (bool, optional): Allows to raise error if the dir exists.

        Examples:
            Create parents for a file without creating the file:
                utils.create_dir(Path("exports/reports/results.csv"))

            Create a directory and any missing ancestors:
                utils.create_dir(Path("exports/reports"), is_file=False)
        """
        directory = path.parent if is_file else path
        directory.mkdir(parents=True, exist_ok=exist_ok)
    
    def validate_json(
        self,
        obj: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        """
        Require an object to be a Python dictionary.
        
        This checks the top-level type only. It does not validate nested
        values, key types, JSON serializability, or an application schema.

        Args:
            obj (Dict[Any, Any]): Object to check as a JSON object representation.

        Returns:
            Dict[Any, Any]: The original dictionary, without copying or changes.
        """
        if not isinstance(obj, dict):
            raise ValueError(
                "Object must be an appropriate dictionary object."
            )
        return obj
    
    def read_json(
        self,
        path: Path,
        encoding: str = "utf-8",
    ) -> Dict[Any, Any]:
        """
        Decode a non-empty JSON file and require a top-level object.
        
        The complete JSON document is loaded into memory. Dates, paths,
        and other application-specific types are not reconstructed from
        their serialized representations.

        Args:
            path (Path): Existing, non-empty file containing JSON. The suffix
                is not checked.
            encoding (str, optional): Text encoding used to open the file.
                Defaults to "utf-8".

        Returns:
            Dict[Any, Any]: Decoded top-level JSON object as a dictionary.
        """
        self.validate_file_path(path=path)
        self.validate_format(path=path, supported_formats=[".json"])
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
        Serialize an object as indented JSON at the destination path.
        
        Output uses four-space indentation and preserves non-ASCII
        characters rather than escaping them. Standard encoder defaults
        apply, including allowing NaN and infinity tokens.

        Convert unsupported values such as datetime, Path, and Decimal to
        JSON-compatible representations before calling this method. Writes
        are not atomic: an encoding or serialization failure may leave an
        existing destination truncated or partially written.

        Args:
            obj (Dict[Any, Any]): Object to encode with the standard JSON
                encoder. Dictionary input is expected but is not validated.
            path (Path): Destination file. Missing parent directories are
                created and an existing file is overwritten. No suffix check
                is performed.
            encoding (str, optional): Text encoding used to write the file.
                Defaults to "utf-8".
        """
        self.validate_format(path=path, supported_formats=[".json"])
        self.create_dir(path=path)
        with open(str(path), "w", encoding=encoding) as file:
            json.dump(obj, file, indent=4, ensure_ascii=False, allow_nan=True)
