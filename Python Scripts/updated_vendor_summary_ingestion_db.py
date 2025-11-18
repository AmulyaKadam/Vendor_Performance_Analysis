import os
import urllib.parse
from sqlalchemy import create_engine, text
import pandas as pd
import logging


# ====== DATABASE CONNECTION ======
username = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD")   # store securely in env var
database = os.getenv("MYSQL_DB", "inventory")

encoded_password = urllib.parse.quote_plus(password or "")
engine = create_engine(
    f"mysql+pymysql://{username}:{encoded_password}@localhost:3306/{database}",
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)


# ====== LOGGING CONFIG ======
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# ====== CREATE SUMMARY QUERY ======
def create_vendor_summary(conn):
    """Merge tables to get overall vendor summary and add derived columns."""
    query = '''
        WITH FreightSummary AS (
            SELECT 
                VendorNumber, 
                SUM(Freight) AS FreightCost 
            FROM vendor_invoice 
            GROUP BY VendorNumber
        ), 

        PurchaseSummary AS (
            SELECT 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp
                ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
        ), 

        SalesSummary AS (
            SELECT 
                VendorNo,
                Brand,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        ) 

        SELECT 
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.PurchasePrice,
            ps.ActualPrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss 
            ON ps.VendorNumber = ss.VendorNo 
            AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs 
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
    '''
    return pd.read_sql(query, conn)


# ====== CLEAN DATA ======
def clean_data(df):
    """Create calculated metrics and clean up data for ingestion."""
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1)) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)

    df['Volume'] = df['Volume'].astype(float)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    df.fillna(0, inplace=True)
    return df


# ====== INGEST FUNCTION ======
def ingest_db(df, table_name, engine):
    """
    Ingests a DataFrame into a database table efficiently.
    Uses engine.begin() for proper commit.
    """
    with engine.begin() as conn:  # auto-committing context
        conn.execute(text(f"TRUNCATE TABLE {table_name}"))
        df.to_sql(
            table_name,
            con=conn,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=2000
        )
        # verify count after insert
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f" Ingested {count:,} rows into '{table_name}'.")
        logging.info(f" Ingested {count:,} rows into '{table_name}'.")


# ====== MAIN EXECUTION ======
if __name__ == "__main__":
    with engine.connect() as conn:
        current_db = conn.execute(text("SELECT DATABASE();")).scalar()
        print(f" Connected to database: {current_db}")
        logging.info(f" Connected to database: {current_db}")

    try:
        with engine.connect() as conn:
            logging.info(" Creating Vendor Summary Table...")
            summary_df = create_vendor_summary(conn)
            logging.info(f"Sample summary data:\n{summary_df.head()}")

        logging.info(" Cleaning Data...")
        clean_df = clean_data(summary_df)
        logging.info(f"Cleaned data sample:\n{clean_df.head()}")

        logging.info(" Ingesting Data...")
        ingest_db(clean_df, "vendor_sales_summary", engine)
        logging.info(" ETL Completed Successfully.")

    except Exception as e:
        logging.error(f" Script failed: {e}", exc_info=True)
        print(f" Script failed: {e}")
