"""
utils/file_utils/audio_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling audio data.
"""
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class AudioFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the audio file utils.
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
    
    def open_reader(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def open_writer(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def close_reader(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def close_writer(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def list_stream(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_segment(
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
    
    def read_tags(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_tags(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError

    def stream_audio(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def transcode_file(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
