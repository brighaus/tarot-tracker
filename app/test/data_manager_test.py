import os
import unittest
import app.data_manager as data_manager

class DataManagerTestCase(unittest.TestCase):
    """tests for data_manager.py"""
    @classmethod
    def setUpClass(cls):
        cls.datamgr = data_manager.DataManager()
        cls.db = 'test_db'
        cls.test_data = {'1': "foo",
                          '2': "bar",
                          '3': "bat"}
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db)

    def test_cache_new_instance(self):
        """does creating a new instance require a cache refresh? """
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_cache_write_db(self):
        """does writing a new db require a cache refresh?"""
        self.datamgr.write_db(self.test_data, self.db)
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_cache_refreshed(self):
        """does get_cache refresh stale cache? """
        testcache = self.datamgr.get_cache(self.db)
        self.assertFalse(self.datamgr.is_get_db)
    
    def test_cache_update_member(self):
        """does the cache need refresh after member update?"""
        self.datamgr.update_db_member('i have been changed', '1', shelve_target=self.db)
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_can_read_db(self):
        """can the data in the cache be accessed?"""
        testdata = self.datamgr.get_cache(shelve_target=self.db)
        self.assertTrue(testdata)

if __name__ == '__main__':
    unittest.main()
