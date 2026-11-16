

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

# DatabaseManager class to handle database operations such as 
# creating tables and managing connections

# Returns a DatabaseManager instance with an active database connection

class DatabaseManager:
    
    def __init__(self):
        
        # Initialize the database connection
        try:
            self.conn = psycopg.connect(host="postgres",
                                        dbname="invoices",
                                        user="maart",
                                        password="maart123")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise DatabaseConnectionException(f"Failed to connect to the database: {e}") from e
      
    def create_invoice_table(self):
            
            # Create the invoices table if it doesn't exist and insert the provided invoice data
            
            try:
                
                query="""
                    CREATE TABLE IF NOT EXISTS invoices (
                        id SERIAL PRIMARY KEY,
                        leverancier TEXT,
                        factuurnummer TEXT,
                        datum DATE,
                        totaal_ex_btw NUMERIC(10,2),
                        btw_bedrag NUMERIC(10,2),
                        totaal_inclusief NUMERIC(10,2),
                        vertrouwen NUMERIC,
                        aangemaakt TIMESTAMP DEFAULT NOW()
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
                raise TableCreationException(f"Failed to create invoice table: {e}")
                
     
     
    # Method to insert a new invoice into the invoices table
    def insert_invoice(self, leverancier, factuurnummer, 
                       datum, totaal_ex_btw, btw_bedrag, totaal_inclusief, vertrouwen):
        try:
            query = """
                INSERT INTO invoices (leverancier, factuurnummer, 
                datum, totaal_ex_btw, btw_bedrag, totaal_inclusief, vertrouwen)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            with self.conn.cursor() as cursor:
                
                # Execute the query to insert the new invoice into 
                # the invoices table
                
                cursor.execute(query, (leverancier, factuurnummer, datum, totaal_ex_btw, btw_bedrag, totaal_inclusief, vertrouwen))
            
            # Commit the transaction to save the changes
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to insert invoice: {e}")
            
            # Rollback the transaction in case of an error
            self.conn.rollback()
            raise InsertException(f"Failed to insert invoice: {e}")