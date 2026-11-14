"""Integration tests for SQL Sever connectivity"""

import unittest

from incentive_dw.config import DatabaseConfig
from incentive_dw.connection import DatabaseConnection

class TestSQLServerConnection(unittest.TestCase):
  """Tests connectivity to the configured SQL Server database"""
  
  def setUp(self):
    """Create configuration and database connection"""
    self.config = DatabaseConfig()
    self.database = DatabaseConnection(self.config)
    
  def tearDown(self):
    """Release database resources after the test"""
    self.database.close()
    
  def test_database_connection(self):
    """Verify connectivity to the expected database"""
    result = self.database.test_connection()
    
    self.assertEqual(
      result["database_name"],
      self.config.database,
    )
    
    self.assertTrue(result["server_name"])
    
if __name__ == "__main__":
  unittest.main()
    