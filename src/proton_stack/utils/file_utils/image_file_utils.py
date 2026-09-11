"""
utils/file_utils/image_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling image data.
"""
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class ImageFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the image file utils.
        """
        return
    
    @override
    def read_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def save_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def supported_formats(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def validate_path(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def validate_format(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def read_metadata(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def write_metadata(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def verify_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def read_bytes(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def save_bytes(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def convert_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def get_checksum(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_exif(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
