"""
utils/file_utils/text_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling text data.
"""
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class TextFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the text file utils.
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
    
    def iter_chunks(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_chunks(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def iter_lines(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_lines(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def append_text(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def count_lines(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def append_line(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def detect_encoding(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def convert_encoding(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
