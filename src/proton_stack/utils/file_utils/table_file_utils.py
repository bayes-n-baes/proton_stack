"""
utils/file_utils/table_file_utils.py
------------------------------------

The following file contains the basic functionalities 
for handling tabular data.
"""
import pyarrow.ipc as ipc
import pyarrow.parquet as pq
import pyarrow.orc as orc
import polars as pl
import duckdb as db

from io import BytesIO
from pathlib import Path
from typing_extensions import override
from typing import Any, Dict, Iterable, Iterator, List, Union

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
        lazy: bool = False,
        collect: bool = False,
        sheet_name: str = None,
    ) -> Union[pl.DataFrame | pl.LazyFrame]:
        """
        Reads any table with DuckDB and Polars DataFrame.

        Args:
            path (Path): The input path to the file to be read.
            lazy (bool, optional): Ensures Polars LazyFrame is returned. Defaults to False.
            collect (bool, optional): Collects the Polars LazyFrame into Polars \
                DataFrame. Defaults to False.
            sheet_name (str, optional): Only used for *.xlsx files, referes to \
                the sheet to be loaded. Defaults to None.

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
            
        elif "jsonl" in file_suffix:  
            rel = self._read_file_query(
                query=f"SELECT * FROM read_ndjson('{str(path)}')"
            )
            
        elif "json" in file_suffix:  
            rel = self._read_file_query(
                query=f"SELECT * FROM read_json('{str(path)}')"
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
        # If lazy = False, rel is pl.DataFrame else pl.LazyFrame
        rel = rel.pl(lazy=lazy)
        if lazy and collect:
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
            
        elif "jsonl" in file_suffix:
            df.write_ndjson(path)
            
        elif "json" in file_suffix:
            df.write_json(path)
            
        elif "feather" in file_suffix:
            df.write_ipc(path)
            
        elif "arrow" in file_suffix:
            df.write_ipc(path)
            
        elif "orc" in file_suffix:
            orc.write_table(df.to_arrow(), path)
            
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
        self.create_dir(path=path)
        obj = self.read_metadata(df=df)
        self.save_json(obj=obj, path=path)
            
    @override
    def verify_file(
        self,
        path: Path,
        full: bool = False,
        num_rows: int = 1,
    ) -> bool:
        """
        Checks if a file could be loaded.
        Supports two formats, one full and the other partial.

        Args:
            path (Path): The file to be loaded.
            full (bool, optional): Loads the complete file if True else \
                num_rows. Defaults to False.
            num_rows (int): Number of rows to load from the file path. \
                Defaults to 1.

        Returns:
            bool: If the process of loading the file successful.
        """
        try:
            if full:
                self.read_file(path=path)
            else:
                self.preview_file(path=path, num_rows=num_rows)
        except Exception as _:
            return False

        return True
    
    @override
    def read_bytes(
        self,
        data: bytes,
        file_format: str,
        sheet_name: str = None,
    ) -> pl.DataFrame:
        """
        Decodes tabular data stored in an in-memory byte buffer.

        Args:
            data (bytes): The serialized tabular data.
            file_format (str): The data format, with a leading dot.
            sheet_name (str, optional): Sheet to read from an *.xlsx buffer.
                Defaults to None.

        Returns:
            pl.DataFrame: The decoded Polars DataFrame.
        """
        file_format = f".{file_format.lower().lstrip('.')}"
        if file_format not in SUPPORTED_TABLE_FILE_FORMATS:
            raise RuntimeError(
                f"File format: {file_format} is not supported. Supported "
                f"file formats include: {SUPPORTED_TABLE_FILE_FORMATS}"
            )
        buffer = BytesIO(data)

        if "parquet" in file_format:
            return pl.read_parquet(buffer)
        
        elif "csv" in file_format:
            return pl.read_csv(buffer)
        
        elif "tsv" in file_format:
            return pl.read_csv(buffer, separator="\t")
        
        elif "xlsx" in file_format:
            return pl.read_excel(buffer, sheet_name=sheet_name)
        
        elif "jsonl" in file_format:
            return pl.read_ndjson(buffer)
        
        elif "json" in file_format:
            return pl.read_json(buffer)
        
        elif "feather" in file_format:
            return pl.read_ipc(buffer)
        
        elif "arrow" in file_format:
            return pl.read_ipc(buffer)
        
        elif "orc" in file_format:
            return pl.from_arrow(orc.read_table(buffer))
        
        elif "avro" in file_format:
            return pl.read_avro(buffer)

    @override
    def save_bytes(
        self,
        df: pl.DataFrame,
        file_format: str,
        sheet_name: str = "Sheet1",
    ) -> bytes:
        """
        Encodes a Polars DataFrame into an in-memory byte buffer.

        Args:
            df (pl.DataFrame): The DataFrame to encode.
            file_format (str): The output format, with a leading dot.
            sheet_name (str, optional): Sheet name for *.xlsx output.
                Defaults to "Sheet1".

        Returns:
            bytes: The encoded tabular data.
        """
        file_format = f".{file_format.lower().lstrip('.')}"
        if file_format not in SUPPORTED_TABLE_FILE_FORMATS:
            raise RuntimeError(
                f"File format: {file_format} is not supported. Supported "
                f"file formats include: {SUPPORTED_TABLE_FILE_FORMATS}"
            )
        buffer = BytesIO()

        if "parquet" in file_format:
            df.write_parquet(buffer)
        
        elif "csv" in file_format:
            df.write_csv(buffer)
        
        elif "tsv" in file_format:
            df.write_csv(buffer, separator="\t")
        
        elif "xlsx" in file_format:
            df.write_excel(buffer, worksheet=sheet_name)
        
        elif "jsonl" in file_format:
            df.write_ndjson(buffer)
        
        elif "json" in file_format:
            df.write_json(buffer)
        
        elif "feather" in file_format:
            df.write_ipc(buffer)
        
        elif "arrow" in file_format:
            df.write_ipc(buffer)
        
        elif "orc" in file_format:
            orc.write_table(df.to_arrow(), buffer)
        
        elif "avro" in file_format:
            df.write_avro(buffer)

        return buffer.getvalue()
    
    @override
    def convert_file(
        self,
        input_path: Path,
        output_path: Path,
        input_sheet_name: str = None,
        output_sheet_name: str = "Sheet1",
    ) -> None:
        """
        Converts a file from one format to another format.

        Args:
            input_path (Path): The file path to be loaded.
            output_path (Path): The file path in which the loaded file is converted.
            input_sheet_name (str, optional): Input sheet name only if the \
                input_path is *.xlsx. Defaults to None.
            output_sheet_name (str, optional): Output sheet name only if the \
                output_path is *.xlsx. Defaults to "Sheet1".
        """
        df = self.read_file(
            path=input_path, lazy=False, collect=False, sheet_name=input_sheet_name
        )
        self.save_file(
            df=df, path=output_path, sheet_name=output_sheet_name
        )
    
    def scan_file(
        self,
        path: Path,
        sheet_name: str = None,
    ) -> pl.LazyFrame:
        """
        Returns a LazyFrame for any supported table format.

        Args:
            path (Path): The path to the input file.
            sheet_name (str, optional): Worksheet to read for XLSX files.
                Defaults to the first sheet when None.

        Returns:
            pl.LazyFrame: The polars LazyFrame which can be queried and filtered.
        """
        self.validate_file_path(path=path)
        self.validate_format(path=path, supported_formats=SUPPORTED_TABLE_FILE_FORMATS)
        file_suffix = path.suffix.lower()
        
        if "parquet" in file_suffix:
            return pl.scan_parquet(path)
        
        elif "csv" in file_suffix:
            return pl.scan_csv(path)
        
        elif "tsv" in file_suffix:
            return pl.scan_csv(path, separator="\t")
        
        elif "jsonl" in file_suffix:
            return pl.scan_ndjson(path)
        
        elif "json" in file_suffix:
            return pl.read_json(path).lazy()
        
        elif "feather" in file_suffix:
            return pl.scan_ipc(path)
        
        elif "arrow" in file_suffix:
            return pl.scan_ipc(path)
        
        elif "xlsx" in file_suffix:
            return pl.read_excel(path, sheet_name=sheet_name).lazy()
        
        elif "orc" in file_suffix:
            return pl.from_arrow(orc.read_table(path)).lazy()
        
        elif "avro" in file_suffix:
            return pl.read_avro(path).lazy()
    
    def read_schema(
        self,
        path: Path,
    ) -> pl.Schema:
        """
        Retrieves the schema of the data.

        Args:
            path (Path): The input file path.

        Returns:
            pl.Schema: The extracted schema from the file path.
        """
        return self.scan_file(path).collect_schema()
    
    def preview_file(
        self,
        path: Path,
        num_rows: int = 1,
    ) -> pl.DataFrame:
        """
        Scans the table and reads top n rows.

        Args:
            path (Path): The input file path.
            num_rows (int, optional): Top n rows to read from the loaded \
                table. Defaults to 1.

        Returns:
            pl.DataFrame: The top-n rows from a table file.
        """
        return self.scan_file(path=path).head(num_rows).collect()
    
    def iter_batches(
        self,
        path: Path,
        batch_size: int = 10_000,
    ) -> Iterator[pl.DataFrame]:
        """
        Lazily reads a table and yields bounded Polars 
        DataFrame batches.

        Args:
            path (Path): The input table path.
            batch_size (int, optional): Maximum target number of \
                rows per batch. Defaults to 10,000.

        Yields:
            pl.DataFrame: The next batch of rows.
        """
        if not isinstance(batch_size, int) or isinstance(batch_size, bool):
            raise TypeError("batch_size must be an integer.")
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0.")

        lazy_df = self.read_file(
            path=path,
            lazy=True,
            collect=False,
        )
        yield from lazy_df.collect_batches(chunk_size=batch_size)

    def write_batches(
        self,
        batches: Iterable[pl.DataFrame],
        path: Path,
        sheet_name: str = "Sheet1",
    ) -> None:
        """
        Writes Polars DataFrame batches to any supported table format.

        Args:
            batches (Iterable[pl.DataFrame]): DataFrame batches with \
                matching schemas.
            path (Path): The output file path.
            sheet_name (str, optional): Worksheet name for XLSX output.
                Defaults to "Sheet1".
        """
        self.validate_format(path=path, supported_formats=SUPPORTED_TABLE_FILE_FORMATS)
        self.create_dir(path=path)
        iterator = iter(batches)
        try:
            first_batch = next(iterator)
        except StopIteration as exc:
            raise ValueError(
                "batches must contain at least one DataFrame."
            ) from exc

        if not isinstance(first_batch, pl.DataFrame):
            raise TypeError(
                "Every batch must be a Polars DataFrame."
            )

        expected_schema = first_batch.schema
        file_suffix = path.suffix.lower()

        def checked_batches() -> Iterator[pl.DataFrame]:
            yield first_batch
            for batch in iterator:
                if not isinstance(batch, pl.DataFrame):
                    raise TypeError(
                        "Every batch must be a Polars DataFrame."
                    )
                if batch.schema != expected_schema:
                    raise ValueError(
                        "Every batch must have the same schema as the first batch."
                    )
                yield batch

        if file_suffix == ".parquet":
            writer = pq.ParquetWriter(path, first_batch.to_arrow().schema)
            try:
                for batch in checked_batches():
                    writer.write_table(batch.to_arrow())
            finally:
                writer.close()

        elif file_suffix in [".feather", ".arrow"]:
            with path.open("wb") as file:
                with ipc.new_file(file, first_batch.to_arrow().schema) as writer:
                    for batch in checked_batches():
                        writer.write_table(batch.to_arrow())

        elif file_suffix in [".csv", ".tsv"]:
            separator = "\t" if file_suffix == ".tsv" else ","
            with path.open("wb") as file:
                for index, batch in enumerate(checked_batches()):
                    batch.write_csv(
                        file,
                        include_header=index == 0,
                        separator=separator,
                    )

        elif file_suffix == ".json":
            with path.open("wb") as file:
                file.write(b"[")
                has_records = False
                for batch in checked_batches():
                    payload = batch.write_json().strip()
                    if payload == "[]":
                        continue
                    if has_records:
                        file.write(b",")
                    file.write(payload[1:-1].encode("utf-8"))
                    has_records = True
                file.write(b"]")

        elif file_suffix == ".jsonl":
            with path.open("wb") as file:
                for batch in checked_batches():
                    batch.write_ndjson(file)

        elif file_suffix == ".orc":
            writer = orc.ORCWriter(path)
            try:
                for batch in checked_batches():
                    writer.write(batch.to_arrow())
            finally:
                writer.close()

        elif file_suffix == ".xlsx":
            pl.concat(checked_batches(), rechunk=False).write_excel(
                path,
                worksheet=sheet_name,
            )

        elif file_suffix == ".avro":
            pl.concat(checked_batches(), rechunk=False).write_avro(path)

    def validate_schema(
        self,
        df: pl.DataFrame,
        columns: List[str],
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
