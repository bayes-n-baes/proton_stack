"""
utils/file_utils/constants.py
-----------------------

The following file contains all the constants related 
to the different types of files and their utilities.
Below are the supoprted modalities:
    - Table
    - Image
    - Video
    - Audio
    - Texts
    - Graph
"""
import cv2


TABLE_BACKENDS = ["polars"]  # doesn't support pandas
IMAGE_BACKENDS = ["pil", "opencv", "torchcodec"]
VIDEO_BACKENDS = ["pyav", "opencv", "torchcodec"]
AUDIO_BACKENDS = ["soundfile", "torchcodec"]
IMAGE_AND_VIDEO_FORMATS = {
    "pil": [
        "1",
        "L",
        "LA",
        "P",
        "PA",
        "RGB",
        "RGBA",
        "RGBX",
        "RGBa",
        "La",
        "CMYK",
        "YCbCr",
        "LAB",
        "HSV",
        "I",
        "F",
        "I;16",
        "I;16L",
        "I;16B",
        "I;16N",
    ],
    "pyav": [
        "gray",
        "gray16le",
        "gray16be",
        "rgb24",
        "rgba",
        "rgb0",
        "bgr24",
        "bgra",
        "bgr0",
        "yuv420p",
        "yuv422p",
        "yuv444p",
        "yuv420p10le",
        "yuv422p10le",
        "yuv444p10le",
        "nv12",
        "nv21",
        "pal8",
    ],
    "opencv": [
        "GRAY",
        "BGR",
        "BGRA",
        "RGB",
        "RGBA",
    ],
    "torchcodec": [
        "UNCHANGED",
        "GRAY",
        "GRAY_ALPHA",
        "RGB",
        "RGB_ALPHA",
    ],
}
OPENCV_FORMATS = {
    "BGR": None,
    "BGRA": cv2.COLOR_BGR2BGRA,
    "RGB": cv2.COLOR_BGR2RGB,
    "RGBA": cv2.COLOR_BGR2RGBA,
    "GRAY": cv2.COLOR_BGR2GRAY,
}