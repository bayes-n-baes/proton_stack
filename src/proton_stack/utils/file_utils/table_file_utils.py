"""
utils/file_utils/table_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling tabular data.
"""
import polars as pl
import duckdb as db

from pathlib import Path
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class TableFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the table file utils.
        """
        return
    
    @override
    def read_file(
        self,
        path: Path | str,
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
    
    def scan_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_schema(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def preview_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def count_rows(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def iter_batches(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_batches(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def validate_schema(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError

    def append_rows(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
