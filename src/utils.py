import requests
from bs4 import BeautifulSoup
from src import constants


def get_page_data_from_url(page_url):
    """
    :return soup of the page retrieved

    :param page_url url of the page to be retrieved
    """
    try:
        page = requests.get(page_url)
        if page.status_code == 200:
            html_content = page.text
            return BeautifulSoup(html_content, "lxml")
    except requests.exceptions.RequestException as e:
        print("Get request failed for " + e.request)


def extract_json_from_source(input_object, source_objects, fields_array, is_order=False):
    return_obj = []
    for i in range(len(source_objects)):
        temp_obj = input_object.copy()
        if is_order:
            temp_obj.update({"order": i + 1})
        for entry in fields_array:
            #print(entry)
            splitter = "||"
            if splitter in entry[1]:
                split_array = entry[1].split(splitter)
                value = source_objects[i].get(split_array[0], None)
                if value is not None:
                    if split_array[1].startswith("*"):
                        value = value[0].get(split_array[1][1:], None)
                    else:
                        value = value.get(split_array[1], None)
            else:
                value = source_objects[i].get(entry[1])
            temp_obj.update({entry[0]: value})
        return_obj.append(temp_obj)
    return return_obj


def create_elastic_search_index(input_data, elastic_search_index, elastic_client):
    elastic_client.index(index=elastic_search_index, doc_type='doc', body=input_data)


def delete_all_elastic_index(elastic_client):
    for index in constants.ELASTIC_INDEX_LIST:
        delete_elastic_index(index, elastic_client)


def delete_elastic_index(elastic_search_index, elastic_client):
    elastic_client.indices.delete(index=elastic_search_index, ignore=[400, 404])


def get_last_item(input_param):
    split_input_block = input_param.split("-")
    return split_input_block[split_input_block.__len__() - 1]
