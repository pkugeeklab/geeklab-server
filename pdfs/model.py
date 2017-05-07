from utils import database


def save(table_type, data):
    items = database.db.pdf.find({'type': 'activity'}).sort([('pdfid', -1)])
    count = items.count()
    if count:
        max_id = items[0]['pdfid']
    else:
        max_id = 0
    data['type'] = table_type
    data['pdfid'] = max_id + 1
    res = database.db.pdf.insert_one(data)
    return data
