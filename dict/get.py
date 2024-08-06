data = {
    'Name': 'Runoob',
    'num' : {
        'first_num' : '66',
        'second_num': '70'
        },
    'age': '15'
}

# 依次get
print(data.get('num').get('first_num')) # 66

# 不在字典中时，可以返回默认值 None 或者设置的默认值。即给字典的键值赋初值
print(data.get('height', "No found"))

# 不在字典中时，会触发 KeyError 异常。
print(data['height'])