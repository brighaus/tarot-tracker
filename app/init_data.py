__author__ = 'brighamhausman'

import glob



__RAW_FILE_TARGET__ = 'data/csv/*csv'

def get_text_list(target_path):
    return_list = []
    # build a single list of text from files
    csv_files = glob.glob(target_path)
    for cf in csv_files:
        with open(cf) as data:
            for line in data:
                cleanln = line.rstrip('\n')
                line_segs = cleanln.split(',')
                clean_segs = []
                if len(line_segs[1]) > 0:
                    for item in line_segs:
                        if len(item) > 0:
                            clean_segs.append(item)
                    return_list.append(clean_segs)
    return return_list

# loop list, clean it and export a list of dictionaries
def get_tt_dict(data_list):
    import re
    return_list = []
    pattern = re.compile("[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}")
    for data_set in data_list:
        headers = ['date', 'suit', 'rank', 'reversed']
        if pattern.match(data_set[0]):
            dct = dict(zip(headers, data_set))
            return_list.append(dct)
    return return_list

def get_db(target_path):
    dirty_text_list = get_text_list(target_path)
    # loop list, clean it and export a list of dictionaries
    db = get_tt_dict(dirty_text_list)
    return db


if __name__ == '__main__':
    dirty_text_list = get_text_list(__RAW_FILE_TARGET__)
    print('dirty_text_list' , dirty_text_list)
    # loop list, clean it and export a list of dictionaries
    db = get_tt_dict(dirty_text_list)
    print('db is', db)

    db2 = get_db(__RAW_FILE_TARGET__)
    print('db2 is', db2)