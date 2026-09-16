"""
utils/file_utils/image_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling image data.
"""
from typing_extensions import override
from typing import Any, List

from .base_file_utils import BaseFileUtils
from .constants import (
    SUPPORTED_IMAGE_AND_VIDEO_CONVERSION_FORMATS, 
    SUPPORTED_IMAGE_AND_VIDEO_FILE_FORMATS, 
    SUPPORTED_IMAGE_BACKENDS
)


class ImageFileUtils(BaseFileUtils):
    
    def __init__(
        self,
    ) -> None:
        """
        Initializes the image file utils.
        """
        return
    
    @override
    def read_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def save_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def supported_backends(
        self,
    ) -> List[str]:
        """
        Provides the supported backends within the framework.

        Returns:
            List[str]: The supported backends by this module.
        """
        return SUPPORTED_IMAGE_BACKENDS
    
    @override
    def supported_formats(
        self,
        backend: str,
    ) -> List[str]:
        """
        The backend-specific list of file formats supported by the utils.

        Args:
            backend (str): The backend to be used for loading data.

        Returns:
            List[str]: The supported file formats for a particular backend.
        """
        return SUPPORTED_IMAGE_AND_VIDEO_CONVERSION_FORMATS
    
    @override
    def read_metadata(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def write_metadata(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def verify_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def read_bytes(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def save_bytes(
        self,
    ) -> Any:
        raise NotImplementedError
    
    @override
    def convert_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def read_exif(
        self,
    ) -> Any:
        raise NotImplementedError
