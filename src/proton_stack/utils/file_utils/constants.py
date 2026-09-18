"""
Constants and configurations concerning the different 
types of files and their utilities integrated in this 
package. Below are the supported modalities:
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
from typing import List, Dict


# ===============================================================================================
# Supported backends
# ===============================================================================================
_SUPPORTED_TABLE_BACKENDS: List[str] = ["polars_duckdb"]
_SUPPORTED_IMAGE_BACKENDS: List[str] = ["pil"]
_SUPPORTED_VIDEO_BACKENDS: List[str] = ["pyav", "opencv",]
_SUPPORTED_AUDIO_BACKENDS: List[str] = ["soundfile",]
_SUPPORTED_TEXTS_BACKENDS: List[str] = []
_SUPPORTED_GRAPH_BACKENDS: List[str] = []
_SUPPORTED_DOCUMENT_BACKENDS: List[str] = []
_SUPPORTED_ARRAY_BACKENDS: List[str] = []
_SUPPORTED_GEO_DATA_BACKENDS: List[str] = []
_SUPPORTED_3D_DATA_BACKENDS: List[str] = []
_SUPPORTED_SEQUENCE_BACKENDS: List[str] = []
_SUPPORTED_MOLECULE_BACKENDS: List[str] = []
_SUPPORTED_MEDICAL_BACKENDS: List[str] = []
_SUPPORTED_SIGNAL_BACKENDS: List[str] = []


# ===============================================================================================
# Supported file formats
# ===============================================================================================
# jsonl: Newline-delimited JSON where each line is a separate JSON record.
# feather: Fast columnar binary format optimized for DataFrame interchange.
# arrow: Apache Arrow columnar format for efficient in-memory and cross-language data exchange.
# orc: Columnar storage format optimized for large-scale analytics workloads.
# avro: Row-oriented binary serialization format with embedded schema support.
_SUPPORTED_TABLE_FILE_FORMATS: Dict[str, List[str]] =  {
    "polars_duckdb": [
        ".parquet", ".csv", ".tsv", ".xlsx", ".json", ".jsonl", ".feather", ".arrow", ".orc", ".avro",
    ]
}
_SUPPORTED_IMAGE_FILE_FORMATS: Dict[str, List[str]] = {
    "pil": [
        ".bmp", ".dib", ".gif", ".jfif", ".jpe", ".jpeg", ".avif", ".dds", ".ico", ".jp2", ".j2k",
        ".jpg", ".pbm", ".pgm", ".pnm", ".ppm", ".pfm", ".png", ".apng", ".webp", ".xbm", ".xpm",
        ".jpc", ".jpf", ".jpx", ".j2c", ".pcx", ".psd", ".qoi", ".tga", ".tif", ".tiff", ".emf",
        ".blp", ".cur", ".dcx", ".eps", ".fits", ".fli", ".flc", ".fpx", ".gbr", ".icns", ".wmf",
        ".im", ".mic", ".mpo", ".msp", ".pcd", ".sgi", 
    ],
}
_SUPPORTED_VIDEO_FILE_FORMATS: Dict[str, List[str]] = {
    "pyav": [
        ".avi", ".mp4", ".m4v", ".mov", ".mkv", ".webm", ".mpg", ".mpeg", ".wmv",
        ".flv", ".ts", ".mts", ".m2ts", ".3gp", ".ogv",
    ],
}


# ===============================================================================================
# Supported conversion formats
# ===============================================================================================
_SUPPORTED_IMAGE_CONVERSION_FORMATS: Dict[str, List[str]] = {
    "pil": [
        "1",      # 1-bit pixels, black and white, stored with one pixel per byte
        "L",      # 8-bit pixels, black and white (grayscale)
        "LA",     # 8-bit pixels, black and white with alpha (transparency) channel
        "P",      # 8-bit pixels, mapped to any other mode using a color palette
        "PA",     # 8-bit pixels, mapped to a color palette with an alpha channel
        "RGB",    # 3x8-bit pixels, true color standard Red, Green, Blue
        "RGBA",   # 4x8-bit pixels, true color Red, Green, Blue with alpha channel
        "RGBX",   # 4x8-bit pixels, true color Red, Green, Blue with padding
        "RGBa",   # 4x8-bit pixels, true color Red, Green, Blue with premultiplied alpha
        "La",     # 8-bit grayscale pixel with premultiplied alpha channel
        "CMYK",   # 4x8-bit pixels, Cyan, Magenta, Yellow, Black color separation
        "YCbCr",  # 3x8-bit pixels, Luminance (Y) and Chrominance (Cb, Cr) color video format
        "LAB",    # 3x8-bit pixels, CIE L*a*b* perceptually uniform color space
        "HSV",    # 3x8-bit pixels, Hue, Saturation, Value color space
        "I",      # 32-bit signed integer pixels
        "F",      # 32-bit floating point pixels
        "I;16",   # 16-bit unsigned integer pixels
        "I;16L",  # 16-bit unsigned integer pixels, little-endian byte order
        "I;16B",  # 16-bit unsigned integer pixels, big-endian byte order
        "I;16N",  # 16-bit unsigned integer pixels, native host byte order
        "I;16S",  # 16-bit signed integer pixels, native host byte order
        "BGR;15", # 15-bit True Color, Blue, Green, Red packaged into 2 bytes
        "BGR;16", # 16-bit True Color, Blue, Green, Red packaged into 2 bytes
        "BGR;24", # 24-bit True Color, standard Blue, Green, Red layout
    ],
}
_SUPPORTED_VIDEO_CONVERSION_FORMATS: Dict[str, List[str]] = {
    "pyav": [
        "gray", "gray16le", "gray16be", "rgb24", "rgba", "rgb0", "bgr24",
        "bgra", "bgr0", "yuv420p", "yuv422p", "yuv444p", "yuv420p10le", 
        "yuv422p10le", "yuv444p10le", "nv12", "nv21", "pal8",
    ],
}
_SUPPORTED_AUDIO_CONVERSION_FORMATS: Dict[str, List[str]] = {
    
}
_SUPPORTED_AUDIO_FILE_FORMATS: Dict[str, List[str]] = {
    
}
_SUPPORTED_TEXTS_FILE_FORMATS: Dict[str, List[str]] = {
    
}
_SUPPORTED_GRAPH_FILE_FORMATS: Dict[str, List[str]] = {
    
}
