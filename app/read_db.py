__author__ = 'brighamhausman'
import shelve
import db_config
import pprint
import sys,argparse

__TARGET__ = db_config.DB_SHELF

def get_db():
    cache_db = {}
    with shelve.open(__TARGET__) as db:
        for key in db:
            cache_db[key] = db[key]
    return cache_db

def dump_db(target=None):
    db = get_db()
    # if no target, assume stdout
    if target is None:
        pprint.pprint(db)
    #TODO: else dump to file @ target

def get_db_members(params={'key':None, 'val':None}):
    # params is a key:value search config
    db = get_db()
    return {result: db[result] for result in db if params['key'] in db[result] and db[result][params['key']] == params['val']}


def test():
    # return list of results
    test_results = get_db()
    return test_results


def main(argv):

    parser = argparse.ArgumentParser(description='DB reading utilities')
    # optional arg that sets a default value on the arg. long and short options
    #parser.add_argument('-v', '--verbose', help='make output more verbose',
    #                   action='store_true')
    parser.add_argument('-d', '--dumpdb', help='gets the db from cache, displays or writes to file',
                        action='store_true')
    parser.add_argument('--target', help='define a target file to dump the query results')
    parser.add_argument('-t', '--test', help='execute self test',
                        action='store_true')
    parser.add_argument('-q', '--query', help='get a subset of the db',
                        action='store_true')
    parser.add_argument('-k','--key', help='query search key')
    parser.add_argument('-v','--val', help='query search value')

    args = parser.parse_args()
    if args.dumpdb:
        db = get_db()
        if args.target:
            with open(args.target, 'w') as target_location:
                target_location.write(str(db))

        # if target no target
        else:
            pprint.pprint(db)
    elif args.test:
        testresult = test()
        for result in testresult:
            print(result)

    elif args.query:
        if args.key and args.val:
            q_params = {'key': args.key, 'val': args.val}
            q_result = get_db_members(q_params)
            for member in list(q_result):
                print(member)
                print('\t', str(q_result[member]))
                print('-------------------')
        else:
            print('key and val arguments are required to run a query')
    else:
        print('auto execute self test...')
        for result in test():
            print(result)

    return 1

if (__name__ == "__main__"):
    #we call the main function passing a list of args, and exit with the return code passed back.
    sys.exit(main(sys.argv))