"""
utils/file_utils/graph_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling graph data.
"""
from typing_extensions import override
from typing import Any

from .base_file_utils import BaseFileUtils


class GraphFileUtils(BaseFileUtils):
    
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the graph file utils.
        """
    
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
    
    def read_edge_list(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_edge_list(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_nodes_edges(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_nodes_edges(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_adjacency(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_adjacency(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_graph_schema(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def read_manifest(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
    
    def write_manifest(
        self,
        *args,
        **kwargs,
    ) -> Any:
        raise NotImplementedError
