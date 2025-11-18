import pandas as pd
from sqlalchemy import create_engine, text, Table, Column, MetaData
from sqlalchemy.types import Integer, String, Float, DateTime, Boolean, Text
import os
import logging
import urllib.parse
import time

# ------------------- Logging Setup -------------------
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file_path = os.path.join(log_folder, "csv_to_mysql.log")

    # ✅ File logs in UTF-8 (supports arrows, emojis, etc.)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # ✅ Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

# ------------------- Config -------------------
folder_path = r"D:\Projects\Music_store_Project\Cvs_files"

# Build csv_files list dynamically
csv_files = [
    (file, os.path.splitext(file)[0])
    for file in os.listdir(folder_path)
    if file.lower().endswith(".csv")
]

# ------------------- Database Engine -------------------
username = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD")   # store in environment variable
database = os.getenv("MYSQL_DB", "music_database")

encoded_password = urllib.parse.quote_plus(password)

engine = create_engine(
    f"mysql+pymysql://{username}:{encoded_password}@localhost:3306/{database}",
    echo=False,
    pool_size=10,
    max_overflow=20
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# ------------------- Helpers -------------------
def sanitize_name(name: str) -> str:
    """Sanitize table/column names for MySQL."""
    name = name.strip().lower()
    for ch in [" ", "-", ".", "/"]:
        name = name.replace(ch, "_")
    return name

def infer_sqlalchemy_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer()
    elif pd.api.types.is_float_dtype(dtype):
        return Float()
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return DateTime()
    elif pd.api.types.is_object_dtype(dtype):
        return Text()
    else:
        return String(255)

def create_table_from_csv(df, table_name, conn):
    metadata = MetaData()
    metadata.reflect(bind=conn)

    table_name = sanitize_name(table_name)

    if table_name in metadata.tables:
        logging.info(f"Table `{table_name}` exists, skipping creation.")
        return table_name

    columns = [Column(sanitize_name(col), infer_sqlalchemy_type(df[col].dtype)) for col in df.columns]
    table = Table(table_name, metadata, *columns)
    metadata.create_all(conn, [table])
    logging.info(f"Created table `{table_name}`")
    return table_name

# ------------------- Date Conversion -------------------
def safe_convert_datetime(series, table_name, col_name):
    """Try ISO format first, fallback to dayfirst=True."""
    converted = pd.to_datetime(series, format="%Y-%m-%d", errors="coerce")
    if converted.notna().sum() / max(1, len(series.dropna())) > 0.5:
        logging.info(f"[{table_name}] Converted '{col_name}' to datetime using ISO format")
        return converted
    # fallback
    converted2 = pd.to_datetime(series, errors="coerce", dayfirst=True)
    if converted2.notna().sum() / max(1, len(series.dropna())) > 0.5:
        logging.info(f"[{table_name}] Converted '{col_name}' to datetime using dayfirst=True fallback")
        return converted2
    return series

def auto_convert_dates(df, table_name):
    """Convert likely date columns based on column name pattern."""
    date_cols = [col for col in df.columns if "date" in col or "dt" in col]
    for col in date_cols:
        if df[col].dtype == 'object':
            df[col] = safe_convert_datetime(df[col], table_name, col)
    return df

# ------------------- ETL Process -------------------
def process_csv_files(chunk_size=10000):
    total_start = time.time()
    total_rows = 0
    file_stats = []

    # Pre-fetch existing tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    existing_tables = set(metadata.tables.keys())

    for csv_file, raw_table_name in csv_files:
        start_time = time.time()
        table_name = sanitize_name(raw_table_name)

        try:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path)
            df.columns = [sanitize_name(col) for col in df.columns]
            df = df.where(pd.notnull(df), None)

            df = auto_convert_dates(df, table_name)

            with engine.begin() as conn:
                if table_name not in existing_tables:
                    create_table_from_csv(df, table_name, conn)
                    existing_tables.add(table_name)

                csv_row_count = len(df)
                logging.info(f"Processing {csv_file} → {table_name}, rows: {csv_row_count}")

                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=chunk_size
                )

                db_row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                logging.info(f"Loaded {csv_row_count} rows into `{table_name}`. Total rows: {db_row_count}")

                total_rows += csv_row_count
                file_stats.append((table_name, csv_row_count, db_row_count))

        except Exception as e:
            logging.error(f"Failed processing {csv_file}: {e}")

        elapsed = time.time() - start_time
        logging.info(f"[{table_name}] Time: {elapsed:.2f}s")

    total_elapsed = time.time() - total_start
    logging.info("====== ETL SUMMARY ======")
    logging.info(f"Total files: {len(file_stats)}, Total rows: {total_rows}")
    for t, csv_count, db_count in file_stats:
        logging.info(f"Table: {t}, CSV rows: {csv_count}, DB rows: {db_count}")
    logging.info(f"ETL completed in {total_elapsed:.2f} seconds.")

# ------------------- Main -------------------
if __name__ == "__main__":
    process_csv_files()
