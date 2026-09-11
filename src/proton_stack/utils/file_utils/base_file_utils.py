"""
utils/file_utils/base_file_utils.py
-----------------------------

The following file contains the BaseFileUtils implementation 
to be inherited by the other modality-based classes.
"""
# Note: abstractmethod operates on a class instance while
# abstractclassmethod operates on the class itself.
#   - abstractmethod calls instance.method()
#   - abstractclassmethod calls class.method()
from abc import abstractmethod
from typing import Any


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
    def supported_formats(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def validate_path(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    def validate_format(
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
