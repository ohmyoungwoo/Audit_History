keyword = 'ab cd ef'
search = []

keyword_list = keyword.split() 
for key in keyword_list:
    search.append('%%{}%%'.format(key))

print(search)