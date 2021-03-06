import pickle
import shelve
import os

""" pickle_mule.py helper module for reading and writing pickled files.
functions:
push_dict - pushes a dictionary to a file that is pickled.
        params: dictionary, string
        return: True on success else raise error

fetch_dict - get contents of a pickled file.
        params: string
        return: dictionary or raises error

to_file - alias for push_dict
        params: object, string

from_file - alias for fetch dict

to_shelf - pushes k/v data blob to a shelve

from_shelf - returns entire contents of a shelve as a dict
        params: string
        return: dictionary

update_shelf_member - sets value of single item in the shelve by key
        params: string, string, object

get_shelf_member - fetches a single item from the shelve by key
    params: string, string
    return object
"""


def push_dict(dict, name):
    """pickle save the dict as name, returns True on success"""
    try:
        output = open(name, 'wb')
        pickle.dump(dict, output)
        output.close()
        return True
    except PicklingError as err:
        raise err


def fetch_dict(name):
    """gets dictionary stored as pickle file name"""
    try:
        source_file = open(name, 'rb')
        return_val = pickle.load(source_file)
        source_file.close()
        return return_val
    except UnpicklingError as err:
        raise err

"""new API, makes file/shelve relationship more semantically clear."""
def to_file(data, handle):
    push_dict(data, handle)

def from_file(handle):
    return fetch_dict(handle)

"""this function expects k/v data"""
def to_shelf(data, handle, obliterate=False):
    try:
        # wipe out the existing db 
        if obliterate:
            os.remove(handle)
            
        with shelve.open(handle) as db:

            for k in data:
                db[k] = data[k]
    except Exception as e:
        raise e
    finally:
        pass


"""dumps entire shelve db into a dict"""
def from_shelf(handle):
    returnme = dict()
    try:
        with shelve.open(handle) as shelve_data:
            for k in shelve_data:
                returnme[k] = shelve_data[k]
    except Exception as e:
        raise e
    finally:
        pass

    return returnme

"""updates a single shelve member by key"""
def update_shelf_member(shelve_handle, key, val):
    try:
        with shelve.open(shelve_handle) as db:
            db[key] = val
    except Exception as e:
        raise e
    finally:
        pass



"""returns object stored at key"""
def get_shelf_member(shelve_handle, key):
    return_val = None
    try:
        with shelve.open(shelve_handle) as db:
            return_val = db[key]
    except Exception as e:
        raise e

    return return_val



"""returns list of shelf keys"""
def get_shelf_keys(shelve_handle):
    return_val = ()
    try:
        with shelve.open(shelve_handle) as db:
            return_val = list(db.keys())
    except Exception as e:
        raise e
    finally:
        pass

    return return_val


def main():
    import os.path
    # file repo
    test_file = 'test_file.pkl'

    # shelve repo
    test_shelve = 'test_shelve'

    #records
    bob = dict(name='Bob Smith', age=42, pay=30000, job='dev')
    sue = dict(name='Sue Sizzle', age=45, pay=40000, job='hdw')
    tom = dict(name='Tom Lesion', age=50, pay=0, job=None)

    shelve_data = {
        'bob': bob,
        'sue': sue,
        'tom': tom
    }
    # to_file
    # clear previous test
    if os.path.isfile(test_file):
        os.remove(test_file)
    to_file(bob, test_file)
    print('write file success:', os.path.isfile(test_file))
    # from_file
    print('file contents:', from_file(test_file))
    # to_shelf
    if os.path.isfile(test_shelve):
        os.remove(test_shelve)
    to_shelf(shelve_data, test_shelve)

    print('shelve write success:', os.path.isfile(test_shelve))

    # from_shelf
    testme = from_shelf(test_shelve)
    for k in testme:
        print(k, testme[k], sep='=>')

    # get_shelf_member:
    key = list(testme.keys())[0]
    val = get_shelf_member(test_shelve, key)
    print('get item from shelve for:', key, val)
    val['job'] = 'Fired'
    update_shelf_member(test_shelve, key, val)
    print('updated value for', key,
          get_shelf_member(test_shelve,key))

    #get_shelf_keys
    keys_list = get_shelf_keys(test_shelve)
    print('keys:', keys_list)

    print('member from keys list:', get_shelf_member(test_shelve,keys_list[0]))

    breakme = from_shelf('oops')
    print('missing shelve test:', breakme)

# self test
if __name__ == '__main__':
    main()