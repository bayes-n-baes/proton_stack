"""
Read, write, inspect, and convert tabular data with Polars and DuckDB.
File extensions select the reader or writer. PyArrow provides ORC and
incremental columnar writers. Supported formats and backend labels are
defined in the sibling constants module.
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
from .constants import _SUPPORTED_TABLE_BACKENDS, _SUPPORTED_TABLE_FILE_FORMATS


class TableFileUtils(BaseFileUtils):
    """
    Provide file, buffer, batch, and metadata operations for tabular data.

    Methods accept Polars DataFrames and pathlib paths. File-based operations
    select formats from case-insensitive suffixes; buffer operations accept an
    explicit format. LazyFrame results do not always imply deferred file I/O:
    see scan_file for formats that require eager loading.

    Reader, writer, filesystem, and optional dependency errors propagate unless
    otherwise documented by the method.
    """
    
    def __init__(
        self,
    ) -> None:
        """
        Initialize the utility through the base-class constructor.
        """
        super().__init__()
        return
    
    def _read_file_query(
        self,
        query: Any,
    ) -> db.DuckDBPyRelation:
        """
        Submit a SQL query to the default DuckDB connection.

        Args:
            query (Any): SQL query accepted by duckdb.sql.

        Returns:
            db.DuckDBPyRelation: Relation produced by the query.
        """
        return db.sql(query)
        
    @override
    def read_file(
        self,
        path: Path,
        lazy: bool = False,
        collect: bool = False,
        sheet_name: str = None,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        """
        Read a supported table file through DuckDB into Polars.

        Args:
            path (Path): Existing, nonempty file with a supported suffix.
            lazy (bool, optional): Request a LazyFrame from the DuckDB relation.
                Defaults to False.
            collect (bool, optional): Collect the result when lazy is True.
                Has no effect when lazy is False. Defaults to False.
            sheet_name (str, optional): XLSX worksheet name; ignored for other
                formats. Defaults to None. The current SQL construction passes
                None as the literal sheet name "None" rather than omitting it.

        Returns:
            Union[pl.DataFrame, pl.LazyFrame]: A LazyFrame only when lazy is True and
                collect is False; otherwise, a materialized DataFrame.

        Raises:
            RuntimeError: If path validation fails or the suffix is unsupported.

        Notes:
            Feather and Arrow reads install and load the nanoarrow community
            extension; ORC reads install and load the orc community extension.
            These operations can require network access and extension permissions.
            Paths and worksheet names are interpolated into SQL without escaping;
            embedded single quotes are not supported safely.
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
        Serialize a DataFrame using the format selected by the output suffix.

        Args:
            df (pl.DataFrame): Table to serialize.
            path (Path): Destination file with a supported suffix.
            sheet_name (str, optional): Worksheet name for XLSX output; ignored
                for other formats. Defaults to "Sheet1".

        Raises:
            RuntimeError: If the output suffix is unsupported.

        Notes:
            Directory preparation is delegated to BaseFileUtils.create_dir.
            JSON output is an array of records; JSONL output contains one record
            per line. Feather and Arrow use the Arrow IPC file format.
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
        Return the configured table backend labels.

        Returns:
            List[str]: The shared SUPPORTED_TABLE_BACKENDS list, not a copy.
        """
        return _SUPPORTED_TABLE_BACKENDS
        
    @override
    def supported_formats(
        self,
    ) -> List[str]:
        """
        Return the supported table file suffixes.

        Returns:
            List[str]: The shared SUPPORTED_TABLE_FILE_FORMATS list of lowercase
                suffixes with leading dots, not a copy.
        """
        return _SUPPORTED_TABLE_FILE_FORMATS

    @override
    def read_metadata(
        self,
        df: pl.DataFrame,
        max_categories: int = 20,
        max_unique_ratio: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Compute table dimensions, column statistics, and data-quality indicators.

        Args:
            df (pl.DataFrame): Materialized table to inspect.
            max_categories (int, optional): Positive maximum number of distinct
                non-null values for the numeric categorical heuristic. Boolean
                arguments are rejected. Defaults to 20.
            max_unique_ratio (float, optional): Maximum ratio of distinct non-null
                values to non-null entries for that heuristic, in [0, 1].
                Defaults to 0.05.

        Returns:
            Dict[str, Any]: Table-level row_count, column_count,
                estimated_memory_mb, num_duplicate_rows, and columns. The columns
                mapping is keyed by column name and contains dtype flags, null
                and distinct counts, numeric summaries, categorical indicators,
                outlier statistics, and string-content statistics. Inapplicable
                statistics are None.

        Raises:
            TypeError: If max_categories is not an integer or max_unique_ratio
                cannot be compared with the numeric bounds.
            ValueError: If max_categories is less than 1 or max_unique_ratio is
                outside [0, 1].

        Notes:
            unique_count includes null as a distinct value. null_percentage uses
            the total row count and is None for a table with no rows.

            For numeric columns, possibly_categorical is True only when both
            thresholds are met. non_null_unique_ratio excludes nulls from its
            numerator and denominator; NaN and infinity are not excluded by this
            heuristic. Both fields are None for non-numeric or all-null columns.
            A False result does not establish that a column is continuous.

            Outliers fall strictly outside [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR], using
            linear quantile interpolation after conversion to Float64. Null,
            NaN, and infinite values are excluded. outlier_percentage uses the
            finite-value count; outlier fields remain None without finite values.
            The other numeric summaries operate on the original series.

            String checks require one or more Unicode letters (alphabetic), or
            letters and numbers (alphanumeric). Percentages use non-null entries;
            empty strings fail both checks. String fields remain None without
            non-null string values. Percentages are expressed on a 0-to-100 scale.

            This method performs whole-table aggregations, including duplicate
            detection, and may require substantial memory for large tables.
        """
        # Numeric outliers use the 1.5 * IQR rule. Null, NaN, and infinite values
        # are excluded from outlier statistics. Alphabetic and alphanumeric
        # checks use Unicode letters and numbers and exclude null values.
        # Numeric columns are possibly categorical when both distinct-value
        # thresholds are met, excluding nulls. This is a heuristic, not a
        # definitive classification. Non-numeric and all-null columns receive
        # None for possibly_categorical and non_null_unique_ratio.
        
        if isinstance(max_categories, bool) or not isinstance(max_categories, int):
            raise TypeError(
                "max_categories must be an integer."
            )
        if max_categories < 1:
            raise ValueError(
                "max_categories must be greater than 0."
            )
        if not 0 <= max_unique_ratio <= 1:
            raise ValueError(
                "max_unique_ratio must be between 0 and 1."
            )

        table_metadata: Dict[str, Any] = {
            "row_count": df.height,
            "column_count": df.width,
            "estimated_memory_mb": df.estimated_size("mb"),
            "num_duplicate_rows": df.height - df.unique().height,
        }

        null_counts = df.null_count().row(0, named=True)
        unique_counts = df.select(pl.all().n_unique()).row(0, named=True)
        any_outlier_mask = pl.Series(
            "is_outlier",
            [False] * df.height,
            dtype=pl.Boolean,
        )
        columns_metadata: Dict[str, Dict[str, Any]] = {}

        for name, dtype in df.schema.items():
            series = df[name]
            is_numeric = dtype.is_numeric()
            is_string = dtype == pl.String
            column_metadata: Dict[str, Any] = {
                "dtype": str(dtype),
                "is_numeric": is_numeric,
                "possibly_categorical": None,
                "non_null_unique_ratio": None,
                "is_string": is_string,
                "null_count": null_counts[name],
                "null_percentage": (
                    100 * null_counts[name] / df.height
                    if df.height else None
                ),
                # Includes null as a distinct value.
                "unique_count": unique_counts[name],
                "min": series.min() if is_numeric else None,
                "max": series.max() if is_numeric else None,
                "mean": series.mean() if is_numeric else None,
                "median": series.median() if is_numeric else None,
                "std": series.std() if is_numeric else None,
                "outlier_count": None,
                "outlier_percentage": None,
                "outlier_lower_bound": None,
                "outlier_upper_bound": None,
                "alphabetic_count": None,
                "alphanumeric_count": None,
                "alphabetic_percentage": None,
                "alphanumeric_percentage": None,
                "is_alphabetic": None,
                "is_alphanumeric": None,
            }

            if is_numeric:
                non_null_count = df.height - null_counts[name]
                if non_null_count > 0:
                    non_null_unique_count = unique_counts[name] - int(null_counts[name] > 0)
                    unique_ratio = non_null_unique_count / non_null_count
                    column_metadata["non_null_unique_ratio"] = unique_ratio
                    column_metadata["possibly_categorical"] = (
                        non_null_unique_count <= max_categories
                        and unique_ratio <= max_unique_ratio
                    )

                numeric_series = series.cast(pl.Float64, strict=False)
                finite_mask = numeric_series.is_finite().fill_null(False)
                finite_values = numeric_series.filter(finite_mask)

                if finite_values.len() > 0:
                    q1 = finite_values.quantile(0.25, interpolation="linear")
                    q3 = finite_values.quantile(0.75, interpolation="linear")
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    outlier_mask = (
                        finite_mask
                        & (
                            (numeric_series < lower_bound)
                            | (numeric_series > upper_bound)
                        ).fill_null(False)
                    )
                    outlier_count = int(outlier_mask.sum())

                    column_metadata.update({
                        "outlier_count": outlier_count,
                        "outlier_percentage": (
                            100 * outlier_count / finite_values.len()
                        ),
                        "outlier_lower_bound": lower_bound,
                        "outlier_upper_bound": upper_bound,
                    })
                    any_outlier_mask = any_outlier_mask | outlier_mask

            if is_string:
                string_values = series.drop_nulls()
                value_count = string_values.len()

                if value_count > 0:
                    alphabetic_count = int(
                        string_values.str.contains(r"^\p{L}+$").sum()
                    )
                    alphanumeric_count = int(
                        string_values.str.contains(
                            r"^[\p{L}\p{N}]+$"
                        ).sum()
                    )
                    column_metadata.update({
                        "alphabetic_count": alphabetic_count,
                        "alphanumeric_count": alphanumeric_count,
                        "alphabetic_percentage": (
                            100 * alphabetic_count / value_count
                        ),
                        "alphanumeric_percentage": (
                            100 * alphanumeric_count / value_count
                        ),
                        "is_alphabetic": alphabetic_count == value_count,
                        "is_alphanumeric": alphanumeric_count == value_count,
                    })

            columns_metadata[name] = column_metadata

        table_metadata["columns"] = columns_metadata
        return table_metadata
    
    @override
    def write_metadata(
        self,
        df: pl.DataFrame,
        path: Path,
    ) -> None:
        """
        Compute metadata with default thresholds and serialize it as JSON.

        Args:
            df (pl.DataFrame): Table to inspect with read_metadata.
            path (Path): Destination file with a .json suffix.

        Raises:
            RuntimeError: If the destination suffix is not .json.
            TypeError: If the resulting metadata contains values unsupported by
                the standard JSON encoder.

        Notes:
            Directory preparation and JSON encoding use the base-class helpers.
            Numeric metadata values are not normalized for JSON serialization.
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
        Check whether a full read or preview completes without an exception.

        Args:
            path (Path): Table file to check.
            full (bool, optional): Read the full table through read_file when
                True; otherwise, use preview_file. Defaults to False.
            num_rows (int, optional): Preview size when full is False. Ignored
                for a full read. Defaults to 1.

        Returns:
            bool: True if the selected operation succeeds, otherwise False.
                All Exception subclasses raised by the operation are suppressed.

        Notes:
            A successful preview does not establish that the entire file is
            readable. For formats with eager scan fallbacks, a preview still
            loads the full table. This does not validate an expected schema.
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
        Deserialize an in-memory table into a Polars DataFrame.

        Args:
            data (bytes): Complete serialized table payload.
            file_format (str): Supported format, case-insensitive and with or
                without a leading dot, such as "parquet" or ".CSV".
            sheet_name (str, optional): XLSX worksheet to read. None selects the
                default first sheet. Ignored for other formats. Defaults to None.

        Returns:
            pl.DataFrame: Materialized table decoded from data.

        Raises:
            RuntimeError: If the normalized format is unsupported.

        Notes:
            JSON expects a JSON table; JSONL uses the newline-delimited reader.
            Feather and Arrow use the IPC file reader. XLSX requires the optional
            dependencies used by the Polars Excel reader.
        """
        file_format = f".{file_format.lower().lstrip('.')}"
        if file_format not in _SUPPORTED_TABLE_FILE_FORMATS:
            raise RuntimeError(
                f"File format: {file_format} is not supported. Supported "
                f"file formats include: {_SUPPORTED_TABLE_FILE_FORMATS}"
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
        Serialize a DataFrame into an in-memory byte buffer.

        Args:
            df (pl.DataFrame): Table to serialize.
            file_format (str): Supported format, case-insensitive and with or
                without a leading dot.
            sheet_name (str, optional): Worksheet name for XLSX output; ignored
                for other formats. Defaults to "Sheet1".

        Returns:
            bytes: Complete serialized payload in the requested format.

        Raises:
            RuntimeError: If the normalized format is unsupported.

        Notes:
            The entire output is buffered in memory. JSON produces an array of
            records; JSONL produces newline-delimited records. Feather and Arrow
            produce IPC files.
        """
        file_format = f".{file_format.lower().lstrip('.')}"
        if file_format not in _SUPPORTED_TABLE_FILE_FORMATS:
            raise RuntimeError(
                f"File format: {file_format} is not supported. Supported "
                f"file formats include: {_SUPPORTED_TABLE_FILE_FORMATS}"
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
        Read a complete table and write it in the destination format.

        Args:
            input_path (Path): Existing, nonempty source table file.
            output_path (Path): Destination file; its suffix selects the format.
            input_sheet_name (str, optional): Source XLSX worksheet, forwarded
                to read_file. Ignored for other formats. Defaults to None.
            output_sheet_name (str, optional): Destination XLSX worksheet.
                Ignored for other formats. Defaults to "Sheet1".

        Notes:
            The source is fully materialized in memory. Conversion preserves the
            table only as supported by the readers and writers; it does not copy
            workbook styling or other format-specific file metadata. Read and
            write failures propagate from read_file and save_file.
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
        Create a queryable LazyFrame from a supported table file.

        Args:
            path (Path): Existing, nonempty file with a supported suffix.
            sheet_name (str, optional): XLSX worksheet to read. None selects the
                first sheet. Ignored for other formats. Defaults to None.

        Returns:
            pl.LazyFrame: Table on which further expressions can be applied
                before collect is called.

        Raises:
            RuntimeError: If path validation fails or the suffix is unsupported.

        Notes:
            Parquet, CSV, TSV, JSONL, Feather, and Arrow use native lazy scanners.
            Feather and Arrow are interpreted as IPC files.

            JSON, XLSX, ORC, and Avro are read eagerly and then converted to a
            LazyFrame. These fallbacks require memory for the entire table and
            cannot push subsequent filters or row limits into the file reader.
            Native scanner errors may surface later, during schema resolution
            or collection.
        """
        self.validate_file_path(path=path)
        self.validate_format(path=path, supported_formats=_SUPPORTED_TABLE_FILE_FORMATS)
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
        Resolve column names and data types through scan_file.

        Args:
            path (Path): Existing, nonempty table file with a supported suffix.

        Returns:
            pl.Schema: Ordered mapping of column names to Polars data types.

        Notes:
            Schema resolution may inspect data. Formats with eager scan_file
            fallbacks load the entire table. XLSX uses the first worksheet.
        """
        return self.scan_file(path).collect_schema()
    
    def preview_file(
        self,
        path: Path,
        num_rows: int = 1,
    ) -> pl.DataFrame:
        """
        Collect the leading rows of a table through scan_file.

        Args:
            path (Path): Existing, nonempty table file with a supported suffix.
            num_rows (int, optional): Row count passed to LazyFrame.head.
                Use a nonnegative value for a bounded preview. Defaults to 1.

        Returns:
            pl.DataFrame: Leading rows, limited by the available table height
                when num_rows is nonnegative.

        Notes:
            Formats with eager scan_file fallbacks load the entire table before
            applying the limit. XLSX uses the first worksheet.
        """
        return self.scan_file(path=path).head(num_rows).collect()
    
    def iter_batches(
        self,
        path: Path,
        batch_size: int = 10_000,
    ) -> Iterator[pl.DataFrame]:
        """
        Yield DataFrame batches from a lazy DuckDB-backed table read.

        Args:
            path (Path): Existing, nonempty table file with a supported suffix.
            batch_size (int, optional): Positive target row count passed to
                LazyFrame.collect_batches as chunk_size. Defaults to 10,000.

        Yields:
            pl.DataFrame: Successive batches produced by the query engine.

        Raises:
            TypeError: If batch_size is not an integer, including bool values.
            ValueError: If batch_size is less than 1.

        Notes:
            Validation and reading begin when the iterator is consumed. Backend
            and file errors propagate during iteration. The requested batch size
            does not bound total memory used by the reader or query engine.
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
        Serialize an iterable of matching DataFrame batches to one file.

        Args:
            batches (Iterable[pl.DataFrame]): Nonempty iterable of DataFrames
                with the same schema as the first batch. Individual batches may
                contain zero rows. The iterable is consumed once.
            path (Path): Destination file with a supported suffix.
            sheet_name (str, optional): Worksheet name for XLSX output; ignored
                for other formats. Defaults to "Sheet1".

        Raises:
            RuntimeError: If the output suffix is unsupported.
            TypeError: If any batch is not a Polars DataFrame.
            ValueError: If batches is empty or a later batch has a different
                schema from the first batch.

        Notes:
            Parquet, IPC, CSV, TSV, JSON, JSONL, and ORC are written incrementally.
            XLSX and Avro concatenate all batches in memory before writing.
            CSV and TSV contain one header; JSON contains a single record array.

            Batch validation occurs during consumption. Writes are not atomic:
            a late failure can leave a partial destination file. Directory
            preparation is delegated to BaseFileUtils.create_dir.
        """
        self.validate_format(path=path, supported_formats=_SUPPORTED_TABLE_FILE_FORMATS)
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
            """Yield the first batch and validate each subsequent batch's type and schema."""
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
        Return requested column names that are absent from a DataFrame.

        Args:
            df (pl.DataFrame): Table whose column names are inspected.
            columns (List[str]): Required names, compared using exact equality.

        Returns:
            List[str]: Missing names in input order, including repeated missing
                names. An empty list means every requested name is present.

        Notes:
            This checks name presence only, not column order or data types.
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
        Return a DataFrame containing the original rows followed by new rows.

        Args:
            df (pl.DataFrame): Table whose schema defines the expected columns.
            new_rows (List[Dict] | pl.DataFrame): Rows to append. Dictionaries
                are converted with df.schema; a DataFrame is concatenated as
                provided and must have a compatible schema.

        Returns:
            pl.DataFrame: Vertically concatenated table. The input DataFrame is
                not modified.

        Notes:
            Dictionary conversion uses the supplied schema: omitted fields may
            become null and fields outside that schema are not retained. Schema
            and value-conversion errors propagate from Polars.
        """
        if isinstance(new_rows, list):
            # Convert from List[Dict] to pl.DataFrame
            new_rows = pl.from_dicts(new_rows, schema=df.schema)
        # If new_rows is a pl.DataFrame, it could directly be 
        # concatenated to the provided dataframe
        return pl.concat([df, new_rows])
