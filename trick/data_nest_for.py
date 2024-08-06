from pprint import pprint
list = [
    {
        'age': 1,
        'name': "wei",
    },
    {
        'age': 10,
        'name': "zheng",
    },
]
new_list = [
    {
        'attribute 1': 1,
        'attribute 2': 2,
        'list_attribute': [
            {
                'dict_key_1': attribute_item["age"],
                'dict_key_2': attribute_item["name"],
            } for attribute_item
            in list
         ]
    }
]
pprint(new_list)