from utils import database


def save(table_type, data):
    items = database.db.pdf.find().sort([('pdfid', -1)])
    count = items.count()
    if count:
        max_id = int(items[0]['pdfid'])
    else:
        max_id = 0
    data['type'] = table_type
    data['pdfid'] = '{:08}'.format(max_id + 1)
    res = database.db.pdf.insert_one(data)
    return data


def get(pdfid):
    data = database.db.pdf.find_one({'pdfid': pdfid})
    print(pdfid, data)
    return data
