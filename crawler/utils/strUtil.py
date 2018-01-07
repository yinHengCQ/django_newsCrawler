#coding=utf-8


def salary_str2int(salary):
    try:
        list_temp = salary.replace('千', '').replace('月', '').replace('万', '').replace('年', '').replace('/', '').split(
            '-')
        if salary.find('月') > 0:
            if salary.find('千') > 0:
                low = int(float(list_temp[0]) * 1000)
                high = int(float(list_temp[1]) * 1000)
            elif salary.find('万') > 0:
                low = int(float(list_temp[0]) * 10000)
                high = int(float(list_temp[1]) * 10000)
            return {'low': low, 'high': high}
        elif salary.find('年') > 0:
            low = int(float(list_temp[0]) * 10000) / 12
            high = int(float(list_temp[1]) * 10000) / 12
            return {'low': low, 'high': high}
    except:
        return {'low': 0, 'high': 0}

def salary_unicode2int(salary):
    try:
        list_temp = salary.replace('千'.decode('utf-8'), '').replace('月'.decode('utf-8'), '').replace(
            '万'.decode('utf-8'), '').replace('年'.decode('utf-8'), '').replace('/', '').split('-')
        if salary.find('月'.decode('utf-8')) > 0:
            if salary.find('千'.decode('utf-8')) > 0:
                low = int(float(list_temp[0]) * 1000)
                high = int(float(list_temp[1]) * 1000)
            elif salary.find('万'.decode('utf-8')) > 0:
                low = int(float(list_temp[0]) * 10000)
                high = int(float(list_temp[1]) * 10000)
            return {'low': low, 'high': high}
        elif salary.find('年'.decode('utf-8')) > 0:
            low = int(float(list_temp[0]) * 10000) / 12
            high = int(float(list_temp[1]) * 10000) / 12
            return {'low': low, 'high': high}
    except:
        return {'low': 0, 'high': 0}