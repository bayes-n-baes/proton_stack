"""
utils/utils/common_utils.py
---------------------------

The following file contains all the common utils.
"""
import json
from pathlib import Path
from typing import Dict, Any

class CommonUtils:
    
    def __init__(
        self,
    ) -> None:
        return
    
    def validate_json(
        self,
        obj: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        raise NotImplementedError
    
    def read_json(
        self,
        path: Path,
    ) -> Dict[Any, Any]:
        raise NotImplementedError
    
    def save_json(
        self,
        obj: Dict[Any, Any],
        path: Path,
    ) -> None:
        raise NotImplementedError