

# DatabaseManager class to handle database operations such as 
# creating tables and managing connections


from psycopg import logger
import psycopg


class DatabaseManager:
    
    def __init__(self, conn):
        
        # Store the database connection for later use
        self.conn = psycopg.connect(host="postgres",
                                    dbname="invoices",
                                    user="maart",
                                    password="maart123")
        if not self.conn:
            raise ValueError("Database connection is not provided")
        
    def create_invoice_table(self):
            
            # Create the invoices table if it doesn't exist and insert the provided invoice data
            
            try:
                
                query="""
                    CREATE TABLE IF NOT EXISTS invoices (
                        id SERIAL PRIMARY KEY,
                        leverancier TEXT,
                        factuurnummer TEXT,
                        datum DATE,
                        totaal_ex_btw NUMERIC,
                        btw_bedrag NUMERIC,
                        totaal_inclusief NUMERIC
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
                
     
     
    # Method to insert a new invoice into the invoices table
    def insert_invoice(self, leverancier, factuurnummer, 
                       datum, totaal_ex_btw, btw_bedrag, totaal_inclusief):
        try:
            query = """
                INSERT INTO invoices (leverancier, factuurnummer, 
                datum, totaal_ex_btw, btw_bedrag, totaal_inclusief)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            with self.conn.cursor() as cursor:
                
                # Execute the query to insert the new invoice into 
                # the invoices table
                
                cursor.execute(query, (leverancier, factuurnummer, datum, totaal_ex_btw, btw_bedrag, totaal_inclusief))
            
            # Commit the transaction to save the changes
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to insert invoice: {e}")
            
            # Rollback the transaction in case of an error
            self.conn.rollback()