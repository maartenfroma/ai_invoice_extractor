

# DatabaseManager class to handle database operations such as 
# creating tables and managing connections


import logging

import psycopg
from custom_exceptions.db_exceptions import InsertException
from custom_exceptions.db_exceptions import DatabaseConnectionException
from custom_exceptions.db_exceptions import UpdateException
from custom_exceptions.db_exceptions import DeleteException
from custom_exceptions.db_exceptions import TableCreationException
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
                invoice_date, due_date, currency, total_ex_vat, vat_amount, total_inc_vat, category, ledger_account, booking_status, source_file, confidence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            with self.conn.cursor() as cursor:
                
                # Execute the query to insert the new invoice into 
                # the invoices table
                
                cursor.execute(query, (invoice.supplier, invoice.supplier_vat_number, invoice.supplier_chamber_of_commerce, invoice.invoice_number, invoice.invoice_date, invoice.due_date, invoice.currency, invoice.total_ex_vat, invoice.vat_amount, invoice.total_inc_vat, invoice.category, invoice.ledger_account, invoice.booking_status, invoice.source_file, invoice.confidence))
            
            # Commit the transaction to save the changes
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to insert invoice: {e}")
            
            # Rollback the transaction in case of an error
            self.conn.rollback()
            raise InsertException(f"Failed to insert invoice: {e}") from e