"""data manager handles the cache and abstracts out the db connection.
This class should know when to refresh the cache and be able to read from and write to the db.
Properties:
__cache 'local cache of the db
__db_configonnection 'read/write to db
__get_db 'true needs pull from db
    use case is when someone updates a single object. write that to the db and refresh the cache.
    you don't need to write the whole db on a single object update."""
import shelve
import app.db_config as db_config
import app.data_mule as data_mule

class DataManager:
    __cache = None
    __get_db = True

    @property
    def is_get_db(self):
        return self.__get_db

    def get_cache(self, shelve_target=db_config.DB_SHELF):
        # shelve_target lets you change default db: dev, stage, prod, test; for instance
        if self.__get_db is True:
            cache_db = {}
            with shelve.open(shelve_target) as db:
                for key in db:
                    cache_db[key] = db[key]
            self.__get_db = False
            self.__cache = cache_db
        return self.__cache


    def update_db_member(self, member, id, shelve_target=db_config.DB_SHELF):
        # what's the right way to keep a local cache in sync?
        # dual updates or refresh from the db?
        self.get_cache(shelve_target)[id] = member
        data_mule.update_shelf_member(shelve_target, id, member)
        self.__get_db = True

    def write_db(self, db_data, db_target, is_append_existing=True):
        if is_append_existing is True:
            data_mule.to_shelf(db_data, db_target)
            self.__get_db = True

#end class

def run_tests():
    pass


if __name__ == '__main__':
    run_tests()
