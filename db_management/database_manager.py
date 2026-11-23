

# DatabaseManager class to handle database operations such as 
# creating tables and managing connections


import logging
import psycopg
from custom_exceptions.db_exceptions import InsertException
from custom_exceptions.db_exceptions import DatabaseConnectionException
from custom_exceptions.db_exceptions import UpdateException
from custom_exceptions.db_exceptions import DeleteException
from custom_exceptions.db_exceptions import TableCreationException

from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

from models.invoice import Invoice

from config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD
# DatabaseManager class to handle database operations such as 
# creating tables and managing connections

# Returns a DatabaseManager instance with an active database connection

class DatabaseManager:
    
    def __init__(self):
        
        # Initialize the database connection
        try:
            self.conn = psycopg.connect(host=DB_HOST,
                                        port=DB_PORT,
                                        dbname=DB_NAME,
                                        user=DB_USER,
                                        password=DB_PASSWORD)
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise DatabaseConnectionException(f"Failed to connect to the database: {e}") from e
      
    def create_invoice_table(self):
            
            # Create the invoices table if it doesn't exist and insert the provided invoice data
            
            try:
                
                query="""
                    CREATE TABLE IF NOT EXISTS invoices (
                        id SERIAL PRIMARY KEY,
                        supplier TEXT,
                        supplier_vat_number TEXT,
                        supplier_chamber_of_commerce TEXT,
                        
                        invoice_number TEXT UNIQUE,
                        invoice_date DATE,
                        due_date DATE,
                        
                        currency VARCHAR(10) DEFAULT 'EUR',
                        
                        total_ex_vat NUMERIC(12,2),
                        vat_amount NUMERIC(12,2),
                        total_inc_vat NUMERIC(12,2),
                        
                        vat_code TEXT,
                        
                        category TEXT,
                        ledger_account TEXT,
                        
                        confidence NUMERIC(5,2),
                        
                        booking_status TEXT DEFAULT 'PENDING',
                        source_file TEXT,
                        
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                """
                
                # Execute the query to create the invoices table if 
                # it doesn't exist
                
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    
                # Commit the transaction to save the changes
                self.conn.commit()  
                
                
            except Exception as e:
                
                logger.error(f"Failed to create invoice table: {e}")
                
                # Rollback the transaction in case of an error
                self.conn.rollback()
                raise TableCreationException(f"Failed to create invoice table: {e}") from e
                
     
     
    # Method to insert a new invoice into the invoices table
    def insert_invoice(self, invoice: Invoice):
        try:
            
            query = """
                INSERT INTO invoices (supplier, supplier_vat_number, supplier_chamber_of_commerce, invoice_number, 
                invoice_date, due_date, currency, total_ex_vat, vat_amount, total_inc_vat, vat_code, category, ledger_account, booking_status, source_file, confidence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with self.conn.cursor() as cursor:
                
                # Execute the query to insert the new invoice into 
                # the invoices table
                cursor.execute(query, (
                    invoice.supplier,
                    invoice.supplier_vat_number,
                    invoice.supplier_chamber_of_commerce,
                    invoice.invoice_number,
                    invoice.invoice_date,
                    invoice.due_date,
                    invoice.currency,
                    invoice.total_ex_vat,
                    invoice.vat_amount,
                    invoice.total_inc_vat,
                    invoice.vat_code,
                    invoice.category,
                    invoice.ledger_account,
                    invoice.booking_status,
                    invoice.source_file,
                    invoice.confidence
                ))
            
            # Commit the transaction to save the changes
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to insert invoice: {e}")
            
            # Rollback the transaction in case of an error
            self.conn.rollback()
            raise InsertException(f"Failed to insert invoice: {e}") from e
           
    
    # Method to retrieve all invoices from the invoices table   
    def get_all_invoices(self):
        
        try:
            query = """
                SELECT
                    supplier,
                    supplier_vat_number,
                    supplier_chamber_of_commerce,
                    invoice_number,
                    invoice_date,
                    due_date,
                    currency,
                    total_ex_vat,
                    vat_amount,
                    total_inc_vat,
                    vat_code,
                    category,
                    ledger_account,
                    confidence,
                    booking_status,
                    source_file
                FROM invoices
                ORDER BY invoice_date DESC
            """

            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)

                rows = cursor.fetchall()

            return rows

        except Exception as e:
            logger.error(f"Failed to get invoices: {e}")
            raise RuntimeError(f"Failed to get invoices: {e}") from e
        
        
    def get_invoice_by_supplier_invoice(self, supplier: str, invoice_number: str):
        
        try:
            query = """
                SELECT *
                   
                FROM invoices
                WHERE supplier = %s AND invoice_number = %s
            """

            with self.conn.cursor() as cursor:
                cursor.execute(query, (supplier, invoice_number))
                row = cursor.fetchone()

            # Return the invoice row if found, None otherwise
            return row

        except Exception as e:
            logger.error(f"Failed to get invoice by supplier and number: {e}")
            raise RuntimeError(f"Failed to get invoice by supplier and number: {e}") from e
        
        
    def get_dashboard_stats(self):
        try:
            query = """
                SELECT
                    COUNT(*) AS invoice_count,
                    COALESCE(SUM(total_inc_vat), 0) AS total_inc_vat,
                    COUNT(DISTINCT supplier) AS supplier_count,
                    COALESCE(SUM(vat_amount), 0) AS vat_total
                    
                FROM invoices
            """

            with self.conn.cursor() as cursor:
                
                cursor.execute(query)
                row = cursor.fetchone()

            # Map the row values to a dictionary for easier access
            return {
                    "invoice_count": row[0],
                    "total_amount": row[1],
                    "supplier_count": row[2],
                    "vat_total": row[3]
                }

        except Exception as e:
            logger.error(f"Failed to get dashboard stats: {e}")
            raise RuntimeError(f"Failed to get dashboard stats: {e}") from e
        
    
    # Get the total invoice amount per supplier
    def get_supplier_totals(self, supplier: str):
        try:
            query = """
                SELECT
                    supplier,
                    COALESCE(SUM(total_inc_vat), 0) AS total_inc_vat
                FROM invoices
              GROUP BY supplier
              ORDER BY total_inc_vat DESC
            """

            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            # Return the list of suppliers with their total invoice amounts
            return rows

        except Exception as e:
            logger.error(f"Failed to get supplier totals: {e}")
            raise RuntimeError(f"Failed to get supplier totals: {e}") from e    