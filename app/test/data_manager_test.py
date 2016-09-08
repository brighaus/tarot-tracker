import os
import unittest
import app.data_manager as data_manager

class DataManagerTestCase(unittest.TestCase):
    """tests for data_manager.py"""
    @classmethod
    def setUpClass(cls):
        print('DataManagerTestCase setting up...')
        cls.datamgr = data_manager.DataManager()
        cls.db = 'test_db'
        cls.test_data = {'1': "foo",
                          '2': "bar",
                          '3': "bat"}
    @classmethod
    def tearDownClass(cls):
        print('DataManagerTestCase tearing down...')
        os.remove(cls.db)

    def test_cache_new_instance(self):
        """does creating a new instance require a cache refresh? """
        print('{}.test_cache_new_instance...'.format(self.__class__.__name__))
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_cache_write_db(self):
        """does writing a new db require a cache refresh?"""
        print('{}.test_cache_write_db...'.format(self.__class__.__name__))
        self.datamgr.write_db(self.test_data, self.db)
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_cache_refreshed(self):
        """does get_cache refresh stale cache? """
        print('{}.test_cache_refreshed...'.format(self.__class__.__name__))
        testcache = self.datamgr.get_cache(self.db)
        self.assertFalse(self.datamgr.is_get_db)
    
    def test_cache_update_member(self):
        """does the cache need refresh after member update?"""
        print('{}.test_cache_update_member...'.format(self.__class__.__name__))
        self.datamgr.update_db_member('i have been changed', '1', shelve_target=self.db)
        self.assertTrue(self.datamgr.is_get_db)
    
    def test_can_read_db(self):
        """can the data in the cache be accessed?"""
        print('{}.test_can_read_db...'.format(self.__class__.__name__))
        testdata = self.datamgr.get_cache(shelve_target=self.db)
        self.assertTrue(testdata)

    # test that a whole new db can be created
    def test_can_create_new_db(self):
        print('{}.test_can_create_new_db...'.format(self.__class__.__name__))
        # start from a common testing point
        olddb = self.datamgr.get_cache(shelve_target=self.db)
        newdb = self.datamgr.get_cache(shelve_target=self.db)
        self.assertTrue(olddb == newdb)
        newdata = {'unit1': 'this is the unit'}
        #destroy existing db create new one
        self.datamgr.write_db(newdata, self.db, obliterate=True)
        newdb = self.datamgr.get_cache(shelve_target=self.db)
        self.assertFalse(olddb == newdb)
    # test that a member can be updated

if __name__ == '__main__':
    unittest.main()
