"""
utils/file_utils/table_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling tabular data.
"""
import pyarrow as pa
import polars as pl
import duckdb as db

from pathlib import Path
from typing_extensions import override
from typing import Any, Union, List, Dict

from .base_file_utils import BaseFileUtils
from .constants import SUPPORTED_TABLE_BACKENDS, SUPPORTED_TABLE_FILE_FORMATS


class TableFileUtils(BaseFileUtils):
    
    def __init__(
        self,
    ) -> None:
        """
        Initializes the table file utils.
        """
        super().__init__()
        return
    
    def _read_file_query(
        self,
        query: Any,
    ) -> db.DuckDBPyRelation:
        return db.sql(query)
        
    @override
    def read_file(
        self,
        path: Path,
        lazy: bool,
        collect: bool,
        sheet_name: str,
    ) -> Union[pl.DataFrame | pl.LazyFrame]:
        """
        Reads any table with DuckDB and Polars DataFrame.

        Args:
            path (Path): The input path to the file to be read.
            lazy (bool): Ensures Polars LazyFrame is returned.
            collect (bool): Collects the Polars LazyFrame into Polars \
                DataFrame.
            sheet_name (str): Only used for *.xlsx files, referes to \
                the sheet to be loaded.

        Returns:
            Union[pl.DataFrame | pl.LazyFrame]: The collected DataFrame or LazyFrame.
        """
        super().validate_file_path(path=path)
        super().validate_format(path=path, supported_formats=self.supported_formats())
        file_suffix: str = path.suffix.lower()
        rel: Union[None, db.DuckDBPyRelation] = None  # holds the relational DB
        
        if "parquet" in file_suffix:
            rel = self._read_file_query(
                query=f"SELECT * FROM read_parquet('{str(path)}')"
            )
            
        elif "csv" in file_suffix:
            rel = self._read_file_query(
                query=f"SELECT * FROM read_csv('{str(path)}')"
            )
            
        elif "tsv" in file_suffix:
            rel = self._read_file_query(
                query=f"SELECT * FROM read_csv('{str(path)}', delim = '\t')"
            )
            
        elif "xlsx" in file_suffix: 
            rel = self._read_file_query(
                query=f"SELECT * FROM read_xlsx('{str(path)}', sheet='{sheet_name}')"
            )
            
        elif "json" in file_suffix:  
            rel = self._read_file_query(
                query=f"SELECT * FROM read_json('{str(path)}')"
            )
            
        elif "jsonl" in file_suffix:  
            rel = self._read_file_query(
                query=f"SELECT * FROM read_ndjson('{str(path)}')"
            )
            
        elif "feather" in file_suffix:  
            db.sql("INSTALL nanoarrow FROM community")
            db.sql("LOAD nanoarrow")
            rel = self._read_file_query(
                query=f"SELECT * FROM read_arrow('{str(path)}')"
            )
            
        elif "arrow" in file_suffix:
            db.sql("INSTALL nanoarrow FROM community")
            db.sql("LOAD nanoarrow")
            rel = self._read_file_query(
                query=f"SELECT * FROM read_arrow('{str(path)}')"
            )
            
        elif "orc" in file_suffix:
            db.sql("INSTALL orc FROM community")
            db.sql("LOAD orc")
            rel = self._read_file_query(
                query=f"SELECT * FROM read_orc('{str(path)}')"
            )
            
        elif "avro" in file_suffix:  
            rel = self._read_file_query(
                query=f"SELECT * FROM read_avro('{str(path)}')"
            )
        
        # db.sql is already lazy with another layer of laziness via pl(lazy=True)
        # lazy = True allows to further filter the data based on conditions, and 
        # later execute .collect() on this
        rel = rel.pl(lazy=lazy)
        if collect:
            # .collect() creates pl.DataFrame out of pl.LazyFrame
            return rel.collect()
        return rel
    
    @override
    def save_file(
        self,
        df: pl.DataFrame,
        path: Path,
        sheet_name: str = "Sheet1",
    ) -> None:
        """
        Saves a Polars DataFrame into the expected file format.

        Args:
            df (pl.DataFrame): The file to be exported and saved.
            path (Path): The output path.
            sheet_name (str, optional): The name of the sheet for *.xlsx \
                files. Defaults to "Sheet1".
        """
        self.validate_format(path=path, supported_formats=self.supported_formats())
        self.create_dir(path=path)
        file_suffix: str = path.suffix.lower()
        
        if "parquet" in file_suffix:
            df.write_parquet(path)
            
        elif "csv" in file_suffix:
            df.write_csv(path)
            
        elif "tsv" in file_suffix:
            df.write_csv(path, separator="\t")
            
        elif "xlsx" in file_suffix: 
            df.write_excel(path, sheet_name)
            
        elif "json" in file_suffix:
            df.write_json(path)
            
        elif "jsonl" in file_suffix:
            df.write_ndjson(path)
            
        elif "feather" in file_suffix:
            df.write_ipc(path)
            
        elif "arrow" in file_suffix:
            df.write_ipc(path)
            
        elif "orc" in file_suffix:
            pa.orc.write_table(df.to_arrow(), path)
            
        elif "avro" in file_suffix:
            df.write_avro(path)
    
    @override
    def supported_backends(
        self,
    ) -> List[str]:
        """
        Retrieves the list of supported backlends.

        Returns:
            List[str]: The list of all the supported table backends.
        """
        return SUPPORTED_TABLE_BACKENDS
        
    @override
    def supported_formats(
        self,
    ) -> List[str]:
        """
        Retrieves the list of supported file formats.

        Returns:
            List[str]: The list of all the supported table file format.
        """
        return SUPPORTED_TABLE_FILE_FORMATS

    @override
    def read_metadata(
        self,
        df: pl.DataFrame
    ) -> Dict[str, Any]:
        """
        Retrieves the metadata from the provided Polars DataFrame.

        Args:
            df (pl.DataFrame): The DataFrame from which metadata \
                is to be extracted.

        Returns:
            Dict[str, Any]: The extracted metadata from the DataFrame.
        """
        table_metadata: Dict[str, Any] = {}
        table_metadata["row_count"] = df.height
        table_metadata["column_count"] = df.width
        table_metadata["estimated_memory_mb"] = df.estimated_size("mb")
        table_metadata["num_duplicate_rows"] = df.height - df.unique().height
        # null_counts holds the column-wise number of nulls
        null_counts = df.null_count().row(0, named=True)
        # unique_counts holds the column-wise number of unique values
        unique_counts = df.select(pl.all().n_unique()).row(0, named=True)
        table_metadata["columns"] = {
            name: {
                "dtype": str(dtype),
                "is_numeric": dtype.is_numeric(),
                "null_count": null_counts[name],
                "null_percentage": (
                    100 * null_counts[name] / df.height
                    if df.height else None
                ),
                # Includes null as a distinct value.
                "unique_count": unique_counts[name],
                "min": df[name].min() if dtype.is_numeric() else None,
                "max": df[name].max() if dtype.is_numeric() else None,
                "mean": df[name].mean() if dtype.is_numeric() else None,
                "median": df[name].median() if dtype.is_numeric() else None,
                "std": df[name].std() if dtype.is_numeric() else None,
            }
            for name, dtype in df.schema.items()
        }
        return table_metadata
    
    @override
    def write_metadata(
        self,
        df: pl.DataFrame,
        path: Path,
    ) -> None:
        """
        Extracts and saves the metadata from a Polars DataFrame.

        Args:
            df (pl.DataFrame): The Polars DataFrame from which metadata \
                needs to be extracted.
            path (Path): The path at which the metadata needs to be saved.
        """
        self.validate_format(path=path, supported_formats=[".json"])
        obj = self.read_metadata(df=df)
        self.save_json(obj=obj, path=path)
            
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
    
    @override
    def get_checksum(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def scan_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def read_schema(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def preview_file(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def count_rows(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def iter_batches(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def write_batches(
        self,
    ) -> Any:
        raise NotImplementedError
    
    def validate_schema(
        self,
        df: pl.DataFrame,
        columns: List[str]
    ) -> List[str]:
        """
        Checks if certain columns in the DataFrame are present.

        Args:
            df (pl.DataFrame): The DataFrame in which th provided \
                columns are to be checked.
            columns (List[str]): The list of column names to find in the \
                provided DataFrame.

        Returns:
            List[str]: The list of column names not in the provided DataFrame.
        """
        all_columns = df.columns
        # Below is an empty list if all column names exist in all_columns
        # Contains column names only when not available in all_columns
        return [
            column for column in columns if column not in all_columns
        ]

    def append_rows(
        self,
        df: pl.DataFrame,
        new_rows: Union[List[Dict], pl.DataFrame],
    ) -> pl.DataFrame:
        """
        Appends new rows to an existing Polars DataFrame.

        Args:
            df (pl.DataFrame): The DataFrame to concatenate new rows to.
            new_rows (Union[List[Dict], pl.DataFrame]): New data needed to be \
                concatenated to the DataFrame.

        Returns:
            pl.DataFrame: Concatenated DataFrame with both old and new rows.
        """
        if isinstance(new_rows, list):
            # Convert from List[Dict] to pl.DataFrame
            new_rows = pl.from_dicts(new_rows, schema=df.schema)
        # If new_rows is a pl.DataFrame, it could directly be 
        # concatenated to the provided dataframe
        return pl.concat([df, new_rows])
