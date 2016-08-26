__author__ = 'brighamhausman'
import init_data
import  db_config
import shelve
import uuid


def dump_db(storage_targ=db_config.DB_SHELF):
    status = []
    dbsrc = init_data.get_db(init_data.__RAW_FILE_TARGET__)
    status.append('looping db' + str(dbsrc))
    with shelve.open(storage_targ) as db:
        for entry in dbsrc:
            id = str(uuid.uuid4())
            db[id] = entry
        status.append('done looping db')
    return status

def dump_test_db():
    return dump_db(db_config.DB_SHELF_TEST)

if __name__ == '__main__':
    db_status = dump_db()
    print('db status', db_status)