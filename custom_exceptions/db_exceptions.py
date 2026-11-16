class DatabaseException(Exception):
    pass

class DatabaseConnectionException(DatabaseException):
    pass

class TableCreationException(DatabaseException):
    pass

class InsertException(DatabaseException):
    pass

class UpdateException(DatabaseException):
    pass

class DeleteException(DatabaseException):
    pass
