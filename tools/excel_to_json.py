# -*- encoding: utf-8 -*-
# @Date   : 2018-06-29
# @Purpose: Transform Excel to Json.
# @Author : Mikoy Chinese

import sys
import locale
import os
import json
import codecs
import xlrd

# Ensure the encoding of System Environment.
__g_codeset = sys.getdefaultencoding()
if 'ascii' == __g_codeset:
    __g_codeset = locale.getdefaultlocale()[1]

# Transform the special sheet of Excel file to json file.


def get_data(file_path):
    # Read the data from excel.
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(u'Fail to read data from excel file: %s' % e)
        return None


def saveFile(file_path, file_name, data):
    output = codecs.open(file_path+'/'+file_name+'.json', 'w', 'utf-8')
    output.write(data)
    output.close()


def excel2json(file_path):
    # Open the excel file.
    if get_data(file_path) is not None:
        book = get_data(file_path)
        # Get all sheet name.
        worksheets = book.sheet_names()
        print('This excel file includes the sheets: \n')
        for sheet in worksheets:
            print('%s, %s' % (worksheets.index(sheet), sheet))
        inp = input(u'Please input the NO of sheet, this sheet will transform '
                    u'to json file automatcicall: \n')
        sheet = book.sheet_by_index((int(inp)))
        row_0 = sheet.row(0)    # The first row is title.
        nrows = sheet.nrows     # Row Number
        ncols = sheet.ncols     # Column Number

        result = []    # Define the json object.
        #result['items'] = []
        #result['rows'] = nrows
        #result['path'] = file_path

        # Walk all rows and convert it to json file.
        for i in range(nrows):
            if i == 0:
                continue
            tmp = {}
            # Walk all columns of the row.
            for j in range(ncols):
                # Get the title of this columns.
                title_de = str(row_0[j])
                title_cn = title_de.split("'")[1]
                # Get the value of cell.
                tmp[title_cn] = sheet.row_values(i)[j]
            result.append(tmp)
        json_data = json.dumps(result, indent=4, sort_keys=True,
                               ensure_ascii=False)
        #json_data = json_data.decode('unicode_escape')

        saveFile(os.getcwd(), worksheets[int(inp)], json_data)
        print(json_data)
        print('\n##########--------Finish---------##########')

if __name__ == '__main__':
    file_path = input(u'Please input the path of excel file:\n')
    json_data = excel2json(file_path)