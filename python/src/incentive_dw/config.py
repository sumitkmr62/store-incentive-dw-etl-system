"""Configuration for the Incentive Data Warehouse Application"""

import os

class DatabaseConfig:

  def __init__(self):
    self.host = os.getenv("SQLSERVER_HOST")
    self.database = os.getenv("SQLSERVER_DATABASE")
    self.driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")

    self.encrypt = os.getenv("SQLSERVER_ENCRYPT", "yes")
    self.trust_server_certificate = os.getenv("SQLSERVER_TRUST_CERTIFICATE", "yes")
    self.trusted_connection = os.getenv("SQLSERVER_TRUSTED_CONNECTION", "yes")

    self._validate_configuration()

  def _validate_configuration(self):
    """Validate required database configuration."""
    if not self.host:
      raise ValueError("SQLSERVER_HOST environment variable is missing.")

    if not self.database:
      raise ValueError("SQLSERVER_DATABASE environment variable is missing.")