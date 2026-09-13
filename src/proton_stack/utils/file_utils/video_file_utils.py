"""
utils/file_utils/video_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling video data.
"""
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class VideoFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the video file utils.
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
    
    @override
    def get_checksum(
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
    
    def read_frames(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def iter_frames(
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
    
    def read_clip(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def extract_frames(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def extract_audio(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def stream_video(
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
