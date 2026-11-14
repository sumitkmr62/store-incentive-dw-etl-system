"""SQL Server connection management using SQLAlchemy Core."""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine
from sqlalchemy.exc import SQLAlchemyError

from incentive_dw.config import DatabaseConfig

class DatabaseConnection:
  """Creates and manages the SQL Server database engine"""
  def __init__(self, config: DatabaseConfig):
    self.config = config
    self.engine = self._create_engine()

  def _create_engine(self) -> Engine:
    """Create a SQLAlchemy Engine using the supplied configuration."""

    connection_url = URL.create(
      drivername="mssql+pyodbc",
      host=self.config.host,
      database=self.config.database,
      query={
        "driver":self.config.driver,
        "Encrypt":self.config.encrypt,
        "TrustServerCertificate":(self.config.trust_server_certificate),
        "trusted_connection":self.config.trusted_connection,
      }
    )
    engine = create_engine(
      connection_url,
      pool_pre_ping=True
    )
    return engine

  def test_connection(self):
    try:
      with self.engine.connect() as connection:
        result = connection.execute(
          text(
            """
               SELECT
                @@SERVERNAME AS server_name,
                DB_NAME() AS database_name
               """
              )
        )
        return result.mappings().one()
    except SQLAlchemyError as error:
      raise ConnectionError(
        "Unable to connect to configured SQL Server Database."
      ) from error

  def close(self):
    """Dispose of SQLAlchemy Engine and its connection pool"""
    self.engine.dispose()
