#!/usr/bin/python3

# GNU license: open to use this code anyway =)

"""
As no user-defined nominal keys >>> PROTOTYPE  =) Message me if not! 'omar.negam@levelupesg.co'

____________________________ Outlines of the code:- 
1. read the lines.
2. statistics on number of blocks using symbol_stack.
[]. locate `;` of the pairs, for any further purpose (e.g., validation)
3-2. split into keys, values stacks.
3-1. filtering braces and commas.
4. collect unique(col_name), corresponding list of values for each.
4-2. refine the type for each column to its value in-place.
5. make all lists of values equal_len by `None` padding.
"""

#From: 2nd year DataStructure material... This is the backbone of the project
class Stack():
    """It is an Abstract Data Type with the operation known as LIFO (or: First In Last Out)."""
    def __init__(self):
        """An empty array created"""
        self.array = []

    def push(self,item):
        """adds the item to the top of the stack."""
        self.array+=[item]

    def pop(self):
        """remove the last added item from the stack, then returns it."""
        poped_item = self.array[-1]
        self.array = self.array[:-1]
        return poped_item


    def peek(self):
        """just returns the last element."""
        return self.array[-1]


    def isNotEmpty(self):
        """`False` if the stack is empty."""
        return bool(self.array)


    def size(self):
        """returns the number of items currently existing in the stack"""
        return len(self.array)

    def get(self):
        """returns the stack as a `list(array)`."""
        return self.array


#////////////////////////////////////////////
#A very special note:
#x.find(char[])                              +1
# +1 because if not found: the find() returns -1, solely treated as True, which is not correct.

# -------------------------------------------------------------------
# I. CONNECTIONS (adjust credentials for your DBs)
# https://jdbc.postgresql.org/documentation/(MANUALLY, to: postgresql-jdbc4 in /usr/share/java)
# 
# -------------------------------------------------------------------
# II. EXTRACT: `sqlline`
# You can't directly extract table data without a query. Even with a special command, `sqlline` must still execute a SQL query behind the scenes to retrieve the data.
"""
!record table_output.txt
!set outputformat table
SELECT * FROM your_table;
!record
"""
# -------------------------------------------------------------------
# III. TRANSFORM

json_symbols = [('"',':',','),  #delimiters and modifiers
                    ('{','['),  #opening braces
                    ('}',']')   #closing braces
    ]

def type_refiner(value,key=None):
    """takes the singular item, whatever it is... except for the lists(they are guaranteed)
    ,   and validates its data type (e.g. removes punctuations from numerical items).
    * For the `key`, it is set BACK for future development to an intelligent validator based on the item keyword."""
    if value in ['[','']:
        return None, type([]).__name__ #Already sit in a list
    elif not value.isnumeric():
        for char in value:
            if char in [c for c in """abcdefghijklmnopqrstuvwxyz!"#$%&'()*+,./;<=>?@\\^_`{|}~"""]:
                #NOTE: found this long string from: [string.ascii_lowercase + string.punctuation] \
                #       and remember... portability, hence no imports ;)
                return value, 'varchar'
            elif char in [':','-']:
                return value, 'date'
            else:
                return value, 'char'
    else:
        if '.' in value:
            value = float(value)
            return value, type(value).__name__
        else:
            value = int(value)
            return value, type(value).__name__
# 25/09/2025
# print('\n\n\n\n\n',k,'\n\n\n\n\n\n')
    # return value,k


with open(input("full_filename: "),'r') as file:# The main header
    # 1. read the lines.
    JSON_lines = list(filter(lambda x: x.find('{"')          +1\
        ,file.readlines()))#NOTE: searches aloooooooooooooooong the file for JSON records.

json_balancer_stack = Stack()   # for the counter operation of the JSON elements.
json_directive_stack = Stack()  # for validating the pairs positions.
json_keys_stack = Stack()       # for column names of the new table.
json_values_stack = Stack()     # for values of each column exists in the current JSON line.

tables_schema = [[] for _ in JSON_lines]    # lists of unique column names to avoid duplication
tables_data = [[] for _ in JSON_lines]      # lists of values(even if lists) for each column name in the tables_schema
unique_schema = []#25/09/2025

for table_no, line in enumerate(list(map(lambda x: x.replace('\n','')
#.split(' ',1)[-1].lstrip() #NOTE: this is file-specific operation
    #                                   , like you NOTICE the definition of the ^above^ stacks.
    #                                   So, it is recommended to have me any thing stripped out surrounding the JSON part.
    ,JSON_lines))):
    #NOTE: table_no, for the logging and the unique lists.
    
    # The JSON counters:
    object_CTR = 0; objray_CTR = 0;
    pair_CTR = 1    #NOTE: because it only counts the delimiters ','.
    
    line = list(line)
    for index, token in enumerate(line):#Here is the counter engine starts up!
        #2. statistics on number of blocks using symbol_stack. 
            
        if token in ['{','[',',']:
            json_balancer_stack.push(token)
            print("at push(with the positional index of the Last_In): ",json_balancer_stack.get(),index) 
        elif token == ':':
            json_directive_stack.push(index)

        if (token in ['}',']']) and ( json_balancer_stack.isNotEmpty()):
            #NOTE: printing current stats in a '\n' at the pop() stage.
            print("before pop: ",json_balancer_stack.get(),'\n',object_CTR, pair_CTR, objray_CTR)
                
            while json_balancer_stack.peek() == ',':
                    pair_CTR += 1
                    json_balancer_stack.pop()
            b = json_balancer_stack.pop()
            if token == '}' and b == '{':
                object_CTR += 1
            elif token == ']' and b == '[':
                objray_CTR += 1

            print("after pop: ",json_balancer_stack.get(),'\n',object_CTR, pair_CTR, objray_CTR)

    print('\n\nFinal stats of the json content (total_n(objects), n(pairs), total_n(arrays)):\n',
                object_CTR, pair_CTR,  objray_CTR)

        #///////////////    Here is the counter engine turns OFF!   \\\\\\\\\\\\\\\\\\\\


# for c in ['[',']','{','}',',']:
# line.remove(c)            #NOTE: but what about Map ?! =)  Here we go:-

    # 3-1. filtering braces and commas.
    mapped_lines = ''.join(list(map(lambda x: x+'\n' if x in ['[',']','{','}',','] else x,line)))
# refined_line = list(filter(lambda x: len(x.strip()) > 1 or x == ' ',mapped_line.split('\n')))      DEPRECATED!


    colon_flag = True           #NOTE: validation process of pairs positions
    for i,v in enumerate(line):
        if v == ':' and colon_flag:
            colon_flag = i in json_directive_stack.get()
            print('actual_index: ',i, 'w.r.t predicted: ',colon_flag)
        elif not colon_flag:
            break
    input(f"######## : INDEXES ARE {colon_flag}! #######\n Press `Enter` or `Ctrl+c` accordingly:");

    json_keys_stack = Stack();  json_values_stack = Stack()

    k_arr_idx = -1 # for checking the 0 position of nested JSON objects

    arr_key = None                     ;   arr_flag = None
        #NOTE: they are FLAGS to decide the parsing whether to turn to normal list or list of objects(dictionaries)
       #arr_key: refers to the dicts       ,   arr_flag: refers to singular values
        
    val_arr = []# to combine the values of the normal list into one element during the parsing process, 
        #which in turn belongs to the same key.

    sub_object_CTR = 1#25/09/2025

        # 3-2. split into keys, values stacks.
    for sub_way in mapped_lines[1:-2].split(','):
#'\n'.join(refined_line)

            #Hey, isn't the following a pipeline =) ?!
        sub_way = sub_way\
                            .replace('{','').replace('}','')\
                                                            .replace('\n','')
            #NOTE: but for ], [ and :  >> they are used for the lists parsing

        pairs = sub_way.split(':',1)#NOTE: cAuTiOn, for misleading text, hold only on the 1st occurrence.
        k = False
        #NOTE: This is because the current `sub_way` may not contain the splitter ':'
        if len(pairs) > 1:
            k,v = pairs
        else:
            v = pairs[0] #NOTE: taking it as a normal string, because split() returns a list object.

    #TODO: intelli_type data refiner!!!
# type_refiner(k,v) #i.e. based on the key namespace

        if (v.find('["')                             +1):
            k += '[]'
            if (v.find(':')                             +1):
            #List of dictionaries
                k2,v = v.split(':')
                arr_flag = None
                k = k#.replace('[','')
                arr_key = k.lstrip()
                k = k2.replace('[','')

#json_keys_stack.pop()
# k = (arr_key + '| ' + k.lstrip()).replace('[','')
# json_keys_stack.push(k.strip().replace('\n','').replace('[',''))

                k_arr_idx = json_keys_stack.get().index(json_keys_stack.peek()) +1
                print(v,"k_arr_idx: ",k_arr_idx)

            else:
                #List of values
                arr_key = None
                v = v.lstrip()
                arr_flag = True
                    
     #BIG NOTICE: `strip()` is the most common operation along the conditions than `replace()`, because it impacts only the char itself, like the Stack, can't get among the values(just the two ends)!!!

        if k:#NOTE: Recall the `if len(pairs)`
            json_keys_stack.push(
                (((((((((((((((((((((((((f'{arr_key}| ' if arr_key else ''))))))))))))))))))))))))) +
                    #NOTE: This is like the `find()                 +1`
                    #                                                 because I frequently forget to add 1*
            #Because, if this part is added at the end without (), the `else` part is the only considered parameter value
                                k.lstrip()
                                        .replace('\n','').replace('"','')
                            )
                
            

        if v.find('"]')                             +1:
            #Close down ANY special parsing:                    
                b_key = []
                for i in range(sub_object_CTR):
                    b_key += [json_keys_stack.pop().replace('[]',f'[{sub_object_CTR}]')]
                       #NOTE instead of slicing, then adding the length, because that key by any fault may NOT have the `[]`, so the function returns INTACT!
                for b in b_key:
                    json_keys_stack.push(b.replace('"',''))

                arr_key = None
                sub_object_CTR = 1

                if arr_flag:#NOTE: for the last element, 
                        # like similar problems where the loop neglects the last elment right at the condition negativity*
                    v = val_arr + [v]
                    b_val = json_keys_stack.pop().replace('[]',f'[{len(v)}]')
                        #NOTE instead of slicing, then adding the length, because that key by any fault may NOT have the `[]`, so the function returns INTACT!
                    json_keys_stack.push(b_val)

# json_values_stack.push()
                arr_flag = None
                val_arr = []
# continue
            
        if arr_key:
            sub_object_CTR += 1

        if arr_flag:#NOTE: The accumulator of the list object.
#: was thought of just an extra assertion  ok?
            val_arr += [v]
            continue

        # 3-3. refine the type for each column to its value in-place.
        v = type_refiner(str(v).lstrip()
                                        .replace('\n','').replace('"','')
                                                                        .replace(']','').replace('[','')                                          
                        ,k)[0]#Native type validator.
        json_values_stack.push(v)
            
# if '[' in list(v):
#     v += ']'     

# json_values_stack.push(v)# if (not arr_flag) else list(json_values_stack.pop())+[v])

    while json_values_stack.size() > pair_CTR:
# print(json_values_stack.size())
        json_values_stack.pop();#NOTE: This for redundancy. ok?
    print('\n\n First look at the ETed table: _duplicates exist_*\n\n')
    print((json_keys_stack.get()),'\n', json_values_stack.get())
    print('First stats: ', json_keys_stack.size(), json_values_stack.size())


        #NOTE: Loading phase: with duplicates removal*
        # 4. collect unique(col_name), corresponding list of values for each.
    for element in json_keys_stack.get():
# [::-1]            
        if (not len(tables_schema[table_no])) or (element not in tables_schema[table_no]):
            tables_schema[table_no] += [element]
                # print(tables_schema[table_no][-1],element)
    for col in tables_schema[table_no]:
        if col not in unique_schema:#25/09/2025
            unique_schema += [col]        
    print('\n\n',f"tables_schema ({len(tables_schema[table_no])}): ",tables_schema[table_no])

        # for val in json_values_stack.get():
    for col in tables_schema[table_no]:
        tables_data[table_no].append([json_values_stack.get()[i] for i,v in enumerate(json_keys_stack.get()) if v == col])

    max_len = 0
        #5. make all lists of values equal_len by `None` padding.
    for sub_t in range(len(tables_data[table_no])):
        element = tables_data[table_no][sub_t]
        if len(element) < max_len:
            while len(tables_data[table_no][sub_t]) < max_len:
                tables_data[table_no][sub_t] += [None]
                    #NOTE: filling the empty lists or missing values with None*(max_len of the longest list)
        else:
            max_len = len(element)

    print('\n\n',f"tables_data ({len(tables_data[table_no])*max_len}) {max_len} item(s)/key: ",tables_data[table_no])


    print('\n__________\n',f"End of JSON record: {table_no}!",'\n__________\n')

print(tables_schema,[len(i) for i in tables_schema], len(unique_schema))#25/09/2025
print(tables_data)


# /****************************************************************************************************BIG TIME
def json_parser(parent_block):
    """TODO: create the same CounTeR using the method of nested functions. DO NOT trust this skeleton 80% !"""
    object_CTR = 0; pair_CTR = 0
    objray_CTR = 0; #NOTE: like `users`

    def object_parser(obj_block):
        nonlocal object_CTR, pair_CTR, objray_CTR

        def pair_parser(pair):
            k, v = tuple(pair.split(':',1))#NOTE:
            if v[0] in json_symbols[1]:
                object_parser(v[1:-1])
            type_refiner(k,v)

        if obj_block[1] == '{':
            objray_CTR += 1
            print(obj_block)
            for entry in obj_block[1:-1].split(',',0):
                input(f"entry {entry}")
                object_CTR += 1
                object_parser(entry)

        elif obj_block[1] == '"':
            print(obj_block)
            for obj in obj_block[1:-1].split(','):
                input(f"obj {obj}")
                pair_CTR += 1
                pair_parser(obj)
    
# print(parent_block[1:-1])
    object_parser(parent_block)
    print(object_CTR, pair_CTR, objray_CTR)
# ****************************************************************************************************/STUDY TIME

"""A sample to try on:
{"section": "Environmental and Social Management System (ESMS)", "score": 4.47, "target": 5.0, "gap": 0.53, "actions": ["Standardize documentation and reporting formats across departments.", "Integrate ESG considerations into enterprise management systems.", "Engage third parties for evaluations or certifications.", "Embed ESG KPIs into strategic planning processes.", "Publish sustainability or impact reports with stakeholder input."]}

Have fun!
"""


# `jp` shell command .......... TBC
# TODO: _Use Shell Scripts to Increase Portability_
# ------------------------------------------------------------------- 
