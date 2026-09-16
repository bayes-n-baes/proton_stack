"""
The following file contains all the constants related 
to the different types of files and their utilities.
Below are the supoprted modalities:
    - Table: Data that exists in rows and columns
    - Image: Data that exists in pixel values
    - Video: Data that exists in sequence of images
    - Audio: Data that exists in time-series waveforms
    - Texts: Data that exists in plain text
    - Graph: Data that exists in nodes and edges
    - Documents:
    - Array:
    - Geo-Data:
    - 3D-Data:
    - Sequences:
    - Molecules:
    - Medical-Data:
    - Signals:
"""
import cv2
from typing import List, Dict


SUPPORTED_TABLE_BACKENDS: List = ["polars + duckdb"]  # doesn't support pandas
SUPPORTED_IMAGE_BACKENDS: List = ["pil", "opencv",]
SUPPORTED_VIDEO_BACKENDS: List = ["pyav", "opencv",]
SUPPORTED_AUDIO_BACKENDS: List = ["soundfile",]
SUPPORTED_TEXTS_BACKENDS: List = []
SUPPORTED_GRAPH_BACKENDS: List = []

SUPPORTED_IMAGE_AND_VIDEO_CONVERSION_FORMATS: Dict = {
    "pil": [
        "1", "L", "LA", "P", "PA", "RGB", "RGBA", "RGBX", "RGBa", "La", 
        "CMYK", "YCbCr", "LAB", "HSV", "I", "F", "I;16", "I;16L", "I;16B", "I;16N",
    ],
    "opencv": [
        "GRAY", "BGR", "BGRA", "RGB", "RGBA",
    ],
    "pyav": [
        "gray", "gray16le", "gray16be", "rgb24", "rgba", "rgb0", "bgr24",
        "bgra", "bgr0", "yuv420p", "yuv422p", "yuv444p", "yuv420p10le", 
        "yuv422p10le", "yuv444p10le", "nv12", "nv21", "pal8",
    ],
}
OPENCV_FORMATS: Dict = {
    "BGR": None,
    "BGRA": cv2.COLOR_BGR2BGRA,
    "RGB": cv2.COLOR_BGR2RGB,
    "RGBA": cv2.COLOR_BGR2RGBA,
    "GRAY": cv2.COLOR_BGR2GRAY,
}
SUPPORTED_AUDIO_CONVERSION_FORMATS: Dict = {
    
}

# jsonl: Newline-delimited JSON where each line is a separate JSON record.
# feather: Fast columnar binary format optimized for DataFrame interchange.
# arrow: Apache Arrow columnar format for efficient in-memory and cross-language data exchange.
# orc: Columnar storage format optimized for large-scale analytics workloads.
# avro: Row-oriented binary serialization format with embedded schema support.
SUPPORTED_TABLE_FILE_FORMATS: List =  [
    ".parquet", ".csv", ".tsv", ".xlsx", ".json", ".jsonl", ".feather", ".arrow", ".orc", ".avro",
]

SUPPORTED_IMAGE_AND_VIDEO_FILE_FORMATS: Dict[str, List[str]] = {
    "pil": [
        ".bmp", ".dib", ".gif", ".jfif", ".jpe", ".jpeg", ".avif", ".dds", ".ico", ".jp2", ".j2k",
        ".jpg", ".pbm", ".pgm", ".pnm", ".ppm", ".pfm", ".png", ".apng", ".webp", ".xbm", ".xpm",
        ".jpc", ".jpf", ".jpx", ".j2c", ".pcx", ".psd", ".qoi", ".tga", ".tif", ".tiff", 
    ],
    "opencv": [
        # Images
        ".bmp", ".dib", ".gif", ".jpeg", ".jpg", ".jpe", ".jp2", ".tif", 
        ".png", ".webp", ".avif", ".pbm", ".pgm", ".ppm", ".pxm", ".tiff",
        ".pnm", ".pfm", ".sr", ".exr", ".hdr", ".pic", ".ras",
        # Videos
        ".avi", ".mp4", ".m4v", ".mov", ".mkv", ".webm", ".mpg", ".mpeg", 
        ".wmv", ".flv", ".ts", ".mts", ".m2ts", ".3gp", ".ogv",
    ],
    "pyav": [
        # Images / image streams supported through FFmpeg
        ".bmp", ".gif", ".jpeg", ".jpg", ".jpe", ".png", ".webp", ".avif", ".tif", ".tiff",

        # Videos
        ".avi", ".mp4", ".m4v", ".mov", ".mkv", ".webm", ".mpg", ".mpeg", ".wmv",
        ".flv", ".ts", ".mts", ".m2ts", ".3gp", ".ogv",
    ],
}
SUPPORTED_AUDIO_FILE_FORMATS: Dict[str, List[str]] = {
    
}
SUPPORTED_TEXTS_FILE_FORMATS: Dict[str, List[str]] = {
    
}
SUPPORTED_GRAPH_FILE_FORMATS: Dict[str, List[str]] = {
    
}
