import urllib.request
import requests
from PIL import Image
import re
import json
import pprint

count = 0
#получаем картинку по url и сохраняем ее в файл
def save_image(url,name_file):
    out = urllib.request.urlopen(url)
    img1 = Image.open(out,'r')
    img1.save(str(name_file)+'.jpg')

def give_params_in_start_page(json_object):
    variables_after = \
    json_object["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"][
        "end_cursor"]
    has_next_page = \
    json_object["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["page_info"][
        "has_next_page"]
    json_object_of_list_image = \
    json_object["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    return variables_after, has_next_page, json_object_of_list_image


def give_params_in_next_page(json_object):
    variables_after = json_object["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
    has_next_page = json_object["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
    json_object_of_list_image = json_object["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
    return variables_after, has_next_page, json_object_of_list_image


def save_image_and_description(json_object_list_items):
    num_element = len(json_object_of_list_image)
    #сохраняем картинку и описание к ней
    for i in range(num_element):#num_element
        global count
        count=count+1
        print(count)
        s = json_object_of_list_image[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
        f = open(str(count)+'.txt', 'w',encoding="utf-8")
        f.write(s)
        save_image(json_object_of_list_image[i]['node']['thumbnail_resources'][4]['src'],count)

# получаем html страницу
page = requests.get('https://www.instagram.com/an.service2018/')
html_text = page.text
reg = 'window._sharedData = .*?</script>'
json_object = re.findall(reg, html_text)[0][21:-10]
json_object = json.loads(json_object)

# преобработка url для автоподгрузки: поиск query_hash и variables для передачи в get
url_for_search_query_hash = "https://www.instagram.com/static/bundles/es6/ProfilePageContainer.js/38a6b4cf0614.js"
page = requests.get(url_for_search_query_hash)
html_text = page.text
query_hash = re.findall("s.pagination},queryId:\".*?\",queryParams",html_text)[0][23:-13]
#query_hash = re.findall("const l=\".*?\",o=r",html_text)[0][9:-5]
variables_id = json_object["entry_data"]["ProfilePage"][0]["logging_page_id"][12:]

variables_after, has_next_page, json_object_of_list_image = give_params_in_start_page(json_object)
save_image_and_description(json_object_of_list_image)

while has_next_page:
    variables = {"id":variables_id, "first":12, "after": variables_after}
    variables = json.dumps(variables)
    params = {'query_hash': str(query_hash), 'variables':variables}
    next_url_page = "https://www.instagram.com/graphql/query/"
    page = requests.get(next_url_page, params=params)
    json_object = page.text
    json_object = json.loads(json_object)
    variables_after, has_next_page, json_object_of_list_image = give_params_in_next_page(json_object)
    save_image_and_description(json_object_of_list_image)




'''
#сохраняем объект window._sharedData
with open('data.txt', 'w') as outfile:
    outfile.write(json.dumps(json_object, indent=4))
pp = pprint.PrettyPrinter(indent=4) #позволяет отобразить json объект в читабельном виде
'''



