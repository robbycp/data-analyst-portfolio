from pandas.io.parsers import TextParser
from lxml.html import parse
import urllib2
import urllib

def _unpack(row, kind='td'):
    '''
    Unpack the html element into string text
    :param row: html element
    :param kind: 
    :return: string text in html element
    '''
    elts = row.findall('.//%s' %kind)
    return [val.text_content().strip() for val in elts]

def parse_options_data(table):
    '''
    Unpack html element and turn it into dataframe
    :param table: html element
    :return: dataframe from the table
    '''
    rows = table.findall('.//tr')
    #print rows
    header = _unpack(rows[0], kind= 'td')
    #print header
    data = [_unpack(r) for r in rows[1:]]
    #print data
    return TextParser(data, names = header).get_chunk()

def response_page(url_target, category):
    '''
    input category to website, and return the html elements response page after the input.
    :param url_target: website to input the category
    :param category: dict of input
    :return: html response page
    '''
    data = urllib.urlencode(category)
    req = urllib2.Request(url_target, data)
    page = urllib2.urlopen(req)
    parsed = parse(page)
    doc = parsed.getroot()
    return doc

def html_to_df(url, list_input):
    '''
    change html data from the response page into table to write on csv, and make
    :param url: website target to be input by list_input
    :param list_input: list of category extracted from seeing the source code
    :param iteration: 
    :return: a table
    '''
    docu = response_page(url, list_input)
    all_table = docu.findall('.//table')

    # exception if the page doesn't exist
    if len(all_table) == 1:
        data = 0
        header = ''
        return data, header

    # making a list of categories of the file for filename
    rows = all_table[0].findall('.//tr')
    categories_list = []
    for row in rows:
        data_file = _unpack(row, kind='td')
        categories_list.append(data_file)
    del categories_list[0]
    del categories_list[-1]
    # test output
    #print categories_list

    # making a filename strings
    header = ""
    for judul in categories_list:
        for teks in judul:
            header = header + teks
        header = header + "_"
    header = header.replace(':', '_')
    header_final = header + '.csv'
    # test output filename
    #print header

    # change html table to dataframe
    table_data_pertanian = all_table[1]
    data_pertanian = parse_options_data(table_data_pertanian)
    # test output dataframe
    #print data_pertanian
    return data_pertanian, header_final

def df_to_csv(data_pertanian, header, pathr):
    #convert dataframe table to csv
    data_pertanian.to_csv(pathr+header)

def html_to_csv(url_target, list_input, iteration, pathr):
    data, header = html_to_df(url_target, list_input)
    if header == '':
        return
    df_to_csv(data, header, pathr)
    print "success %s" % iteration

url = 'http://aplikasi.pertanian.go.id/bdsp/hasil_kom.asp'
list_input = {
    'subsek' : '04',                # hortikultur
    'indikator' : '0104',           # produksi
    'lev_lokasi' : '0',             # nasional
    'propinsi' : '000000',          # hortikultur
    'kabupaten' : '',               # kabupaten
    'status_angka' : '6',           # angka tetap
    'tahun' : '1960'                # 2010-2019
}
pathr = r'E:\hortikultur\coba\\'

'''
# Testing for one page or table to csv
html_to_df(url, list_input)
html_to_csv(url, list_input, 0, pathr)
'''


list_input_hortikultur = [
    ['subsek', '04'],                               # 04 is hortikultur
    ['indikator', '0103', '0104', '0105', '0122'],  # 0103 luas panen, 0104 produksi, 0105 produktivitas,
    # 0122 tanaman menghasilkan
    ['lev_lokasi', '0', '1'],                  # 0 Nasional, 1 provinsi
    ['propinsi', '110000', '120000', '130000', '140000', '150000', '160000', '170000', '180000', '190000',
     '210000', '310000', '320000', '330000', '340000', '350000', '360000', '510000', '520000', '530000',
     '610000', '620000', '630000', '640000', '650000',
     '710000', '720000', '730000', '740000', '750000', '760000'
     '810000', '820000', '910000', '940000'
     ],
    ['status_angka', '6'],                          # 6 is angka tetap
    ['tahun', '1960', '1970', '1980', '1990', '2000', '2010']
]

# Iteration to extract all table from page
iteration = 0
list_input[list_input_hortikultur[0][0]] = list_input_hortikultur[0][1]     # subsek 04
list_input[list_input_hortikultur[4][0]] = list_input_hortikultur[4][1]     # status angka 6


key_indikator = list_input_hortikultur[1][0]
key_lev_lokasi = list_input_hortikultur[2][0]
key_propinsi = list_input_hortikultur[3][0]
key_tahun = list_input_hortikultur[5][0]


for list_indikator in list_input_hortikultur[1][1:]:
    for list_lev_lokasi in list_input_hortikultur[2][1:]:
        if list_lev_lokasi == '0':
            list_propinsi = '000000'
            for list_tahun in list_input_hortikultur[5][1:]:
                list_input[key_indikator] = list_indikator
                list_input[key_lev_lokasi] = list_lev_lokasi
                list_input[key_propinsi] = list_propinsi
                list_input[key_tahun] = list_tahun
                html_to_csv(url, list_input, iteration, pathr)
                iteration += 1
        elif list_lev_lokasi == '1':
            for list_propinsi in list_input_hortikultur[3][1:]:
                for list_tahun in list_input_hortikultur[5][1:]:
                    list_input[key_indikator] = list_indikator
                    list_input[key_lev_lokasi] = list_lev_lokasi
                    list_input[key_propinsi] = list_propinsi
                    list_input[key_tahun] = list_tahun
                    html_to_csv(url, list_input, iteration, pathr)
                    iteration += 1
