import pymongo
import json
import requests
from bs4 import BeautifulSoup

def collect_unifit(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('div.gl-table__inner > div')
    my_dict = {}
    fields = rows[0].select("div")[2:]
    fields = [f.text for f in fields]
    for row in rows[1:]:
        size = row.select("div.gl-table__cell-inner")[0].text
        my_dict[size] = {}
        columns = [r.text for r in row.select("div.gl-table__cell-inner")[0:]]
        for i in range(0, len(columns)):
            my_dict[size][fields[i].replace(u'\xa0', u' ')] = columns[i].replace(u'\xa0', u' ')
    print(my_dict)
    quit()



def collect_tops(response):
    print("here")
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.select("div.size_chart_table > table")
    print(len(table))
    rows = table[0].select('tbody > tr')
    # print(rows)

    first_keys = [l.text for l in rows[0].select("th")[1:]]
    print(first_keys)
    my_dict = {}
    for row in rows[1:]:
        size = row.select("td ")[0].text
        my_dict[size] = {}
        columns = row.select("td ")[1:]
        columns = [c.text for c in columns]
        for i in range(0, len(columns)):
            my_dict[size][first_keys[i].replace(u'\xa0', u' ')] = columns[i].replace(u'\xa0', u' ')
    print(my_dict)

    quit()



def collect_shoes(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("div.size_chart_table > table > tbody > tr")
    my_dict = {}
    first_keys = [l.text for l in rows[0].select("td > strong")]
    second_keys = [w.text for w in rows[1].select("td > strong")]
    print(first_keys)
    for i in range(0, len(first_keys)):
        my_dict[first_keys[i]] = []
    print(my_dict)
    for row in rows[2:]:
        columns = [r.text for r in row.select("td")]
        for i in range(0, len(columns)):
            my_dict[first_keys[i]].append(columns[i].replace(u'\xa0', u' '))
    print(my_dict)
    quit()
    return my_dict

def generic_size(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('div.size_chart_table > table > tbody > tr')
    my_dict = {}
    fields = rows[0].select("th")[0].text
    for row in rows[1:]:
        size = row.select("td ")[0].text
        my_dict[size] = {}
        columns = row.select("td ")[1:]
        columns = [c.text for c in columns]
        for i in range(0, len(columns)):
            my_dict[size][fields[i + 1].replace(u'\xa0', u' ')] = columns[i].replace(u'\xa0', u' ')
    return my_dict

def collect_size_m_tops(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('div.size_chart_table > table > tbody > tr')
    my_dict = {}
    fields = rows[0].select("th")[1:]
    fields = [f.text for f in fields]
    for row in rows[1:]:
        size = row.select("td ")[0].text
        my_dict[size] = {}
        columns = [r.text for r in row.select("td ")[1:]]
        for i in range(0, len(columns)):
            my_dict[size][fields[i].replace(u'\xa0', u' ')] = columns[i].replace(u'\xa0', u' ')
    return my_dict

def hard_coded_sizes(url):
    my_dict = None
    if url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-youth_apparel_8-20":
        my_dict = {"girls": {"S": {"Size": "7-8", "Height": "50-53", "Weight": "53-69"},
                              "M": {"Size": "10-12", "Height": "54-57", "Weight": "70-84"},
                              "L": {"Size": "14", "Height": "58-60", "Weight": "85-99"},
                              "XL": {"Size": "16", "Height": "61-63", "Weight": "100-110"}},
                    "boys": {"S": {"Size": "8-10", "Height": "50-57", "Weight": "59-86"},
                              "M": {"Size": "10-12", "Height": "58-63", "Weight": "87-114"},
                              "L": {"Size": "14-16", "Height": "64-67", "Weight": "115-137"},
                              "XL": {"Size": "18-20", "Height": "68-72", "Weight": "138-150"}}
                    }
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-kids-apparel":
        my_dict = {"Kids' Apparel Size Chart\r\nAges Infant to 7 | Size 3 MO to 7X": {'SIZE': ['3M', '6M', '9M', '12M', '18M', '24M', '2T', '3T', '4T / 4', '5', '6', '6X - 7', '7X'], 'AGE': ['0 - 3 MO', '3 - 6 MO', '6 - 9 MO', '12 MO', '18 MO', '24 MO', '2', '3', '4', '5', '6', '6 - 7', '7'], 'HEIGHT': ['UP TO 23"', '23 - 25"', '25 - 28"', '28 - 31"', '31 - 33"', '33 - 35"', '33 - 35"', '35.5 - 38"', '38.5 - 41"', '41.5 - 44"', '44.5" - 45.5"', '46.5"', '47 - 49"'], 'WEIGHT (LBS)': ['7 - 10', '10 - 13', '13 - 17', '17 - 22', '22 - 25', '25 - 28', '29 - 33', '29 - 33', '34 - 38', '39 - 44', '45 - 49', '50 - 54', '54 - 59']},
                   "Girls' Apparel Size Chart\r\nAges 7 to 12 | Size 7 to 16": {"S": {"SIZE": "7-8", "HEIGHT": "50-53", "WEIGHT": "53-69"}, "M": {"SIZE": "10-12", "HEIGHT": "54-57", "WEIGHT": "70-84"}, "L": {"SIZE": "14", "HEIGHT": "58-60", "WEIGHT": "85-99"}, "XL": {"SIZE": "16", "HEIGHT": "61-63", "WEIGHT": "100-110"}},
                   "Boys' Apparel Size Chart\r\nAges 7 to 12 | Size 8 to 20": {"S": {"SIZE": "8-10", "HEIGHT": "50-57", "WEIGHT": "59-86"}, "M": {"SIZE": "10-12", "HEIGHT": "58-63", "WEIGHT": "87-114"}, "L": {"SIZE": "14-16", "HEIGHT": "64-67", "WEIGHT": "115-137"}, "XL": {"SIZE": "18-20", "HEIGHT": "68-72", "WEIGHT": "138-150"}}}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-calf_sleeve":
        my_dict = {"S/M": {"CALF SLEEVE": "11-14.5"},
                   "L/XL": {"CALF SLEEVE": "14.5-18"}}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-k_shoes":
        my_dict = {'US': ['10.5', '11', '11.5', '12', '12.5', '13', '13.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5', '5.5', '6'], 'UK': ['10', '10.5', '11', '11.5', '12', '12.5', '13', '13.5', '1', '1.5', '2', '2.5', '3', '3.5', ' ', ' ', '', ' '], 'EUROPE': ['28', '28.5', '29', '30', '30.5', '31', '31.5', '32', '33', '33.5', '34', '35', '35.5', '36', '36.7', ' ', ' ', ' '], 'JAPAN': ['175', ' ', '180', '185', ' ', '190', '195', ' ', ' ', ' ', ' ', ' ', ' ', '200', '225', ' ', ' ', ' ']}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-ki_shoes":
        my_dict = {'US': ['0', '1', '2', '3', '4', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10'], 'UK': ['0', '1', '1', '2', '3', '4', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', ' ', ' '], 'EUROPE': [' ', ' ', ' ', ' ', '19', '20', '21', '22', '23', '23.5', '24', '25', '25.5', '26', '26.5', '27'], 'JAPAN': [' ', ' ', ' ', ' ', '120', ' ', ' ', '130', '140', '145', ' ', '150', '155', ' ', '160', '165']}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-shoes":
        my_dict ={'US': ['4', '5', '4.5', '5.5', '5', '6', '5.5', '6.5', '6', '7', '6.5', '7.5', '7', '8', '7.5', '8.5', '8', '9', '8.5', '9.5', '9', '10', '9.5', '10.5', '10', '11', '10.5', '11.5', '11', '12', '11.5', '12.5', '12', '13', '12.5', ' ','13', ' ', '13.5', ' ', '14', ' ', '14.5', ' '], 'UK': ['3.5', '4', '4.5', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12', '12.5', '13', '13.5', '14'], 'EU': ['36', '36.7', '37.3', '38', '38.7', '39.3', '40', '40.7', '41.3', '42', '42.7', '43.3', '44', '44.7', '45.3', '46', '46.7', '47.3', '48', '48.7', '49.3', '50'], 'JP': ['220', '225', '230', '235', '240', '245', '250', '255', '260', '265', '270', '275', '280', '285', '290', '295', '300', '305', '310', '315', '320', '325']}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-w_tops":
        my_dict = {'XXS0 - 2': {'1. BUST': '28.7 - 29.9"', '2. WAIST': '22.4 - 23.6"', '3. HIP': '32.3 - 33.5"'}, 'XS4 - 6': {'1. BUST': '30 - 32"', '2. WAIST': '24 - 26"', '3. HIP': '34 - 36"'}, 'S8 - 10': {'1. BUST': '33 - 35"', '2. WAIST': '27 - 28"', '3. HIP': '37 - 38"'}, 'M12 - 14': {'1. BUST': '36 - 37"', '2. WAIST': '29 - 31"', '3. HIP': '39 - 41"'}, 'L16 - 18': {'1. BUST': '38 - 40"', '2. WAIST': '32 - 34"', '3. HIP': '42 - 43"'}, 'XL20 - 22': {'1. BUST': '41 - 43"', '2. WAIST': '35 - 37"', '3. HIP': '44 - 46"'}, '2XL24 - 26': {'1. BUST': '44 - 46"', '2. WAIST': '38 - 41"', '3. HIP': '47 - 49"'}}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-w_bottoms":
        my_dict = {'XXS0 - 2': {'1. WAIST': '22.4 - 23.6"', '2. HIP': '32.3 - 33.5"', '3. INSEAM': '30.5"'}, 'XS4 - 6': {'1. WAIST': '24 - 26"', '2. HIP': '34 - 36"', '3. INSEAM': '30.7"'}, 'S8 - 10': {'1. WAIST': '27 - 28"', '2. HIP': '37 - 38"', '3. INSEAM': '30.9"'}, 'M12 - 14': {'1. WAIST': '29 - 31"', '2. HIP': '39 - 41"', '3. INSEAM': '31.1"'}, 'L16 - 18': {'1. WAIST': '32 - 34"', '2. HIP': '42 - 43"', '3. INSEAM': '31.3"'}, 'XL20 - 22': {'1. WAIST': '35 - 37"', '2. HIP': '44 - 46"', '3. INSEAM': '31.5"'}, '2XL24 - 26': {'1. WAIST': '38 - 41"', '2. HIP': '47 - 49"', '3. INSEAM': '31.7"'}}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-unitefit_tops":
        my_dict = {'Chest': {'34 (3XS)': '28 3/4 - 30 3/4"', '38 (2XS)': '32 3/4 - 34 3/4"', '42 (XS)': '37 1/2 - 39 1/4"', '46 (S)': '43 - 46 1/2"', '50 (M)': '51 1/2 - 56"', '52 (L)': '56 1/4 - 60 3/4"'}, 'Waist': {'34 (3XS)': '22 1/2 - 23 1/2"', '38(2XS)': '27 1/4 - 28 1/4"', '42 (XS)': '31 - 34 3/4"', '46 (S)': '38 1/4 - 41 3/4"', '50 (M)': '47 1/4 - 52"', '52 (L)': '52 1/4 - 57"'}, 'Hip': {'34 (3XS)': '32 - 33 1/2"', '38 (2XS)': '36 1/4 - 38 1/4"', '42 (XS)': '41 - 43 1/4"', '46 (S)': '46 1/2" - 49 1/4"', '50 (M)': '51 1/2 - 54"', '52 (L)': '54 1/4 - 57"'}}
    elif url == "https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Page-Include?cid=size-chart-size-kg_5-15y":
        my_dict = {"S": {"SIZE": "7-8", "HEIGHT": "50-53", "WEIGHT": "53-69"},
                   "M": {"SIZE": "10-12", "HEIGHT": "54-57", "WEIGHT": "70-84"},
                   "L": {"SIZE": "14", "HEIGHT": "58-60", "WEIGHT": "85-99"},
                   "XL": {"SIZE": "16", "HEIGHT": "61-63", "WEIGHT": "100-110"}}
    return my_dict



text = open("mongo_uri.txt", "r")
mongo_uri = text.read().strip()
text.close()
mongo_db = "remotasks"
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
headers = {
'authority': 'www.adidas.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?0',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-user': '?1',
'sec-fetch-dest': 'document',
'accept-language': 'el-GR,el;q=0.9,en;q=0.8,de;q=0.7,it;q=0.6',
}


# results = db["adidas"].find().distinct("size_chart_link")
# error_counter = 0
# print(results)
# for result in results[1:]:
#     try:
#         my_dict = hard_coded_sizes(result)
#         if my_dict is None:
#             r = requests.get(result, headers=headers)
#             if "size-unitefit_tops" in result:
#                 my_dict = collect_unifit(r)
#             elif "w_bottoms" in result:
#                 my_dict = collect_tops(r)
#             elif "_tops" in result:
#                 my_dict = collect_size_m_tops(r)
#             elif "-shoes" in result:
#                 my_dict = collect_shoes(r)
#             else:
#                 try:
#                     my_dict = collect_size_m_tops(r)
#                 except:
#                     my_dict = generic_size(r)
#                 # my_dict = collect_size_m_tops(r)
#     except Exception as E:
#         error_counter += 1
#         my_dict = None
#         pass
#     up = db["adidas"].update_many({"size_chart_link": result}, {"$set": {"size_chart": my_dict}})
#
# print(error_counter)



results = db["adidas"].find().distinct("id_color")
print(len(results))