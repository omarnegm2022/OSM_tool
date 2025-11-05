#!/usr/bin/python3

# GNU license: open to use this code anyway =)


def main_init(table_no):
    global object_CTR, array_CTR, value_CTR,   sub_object_CTR,sub_key_CTR,              \
        json_balancer_stack, json_directive_stack, json_keys_stack, json_values_stack,  \
        tables_data, tables_schema,unique_schema,   val_arr,                            \
        k_arr_idx,                                                                      \
        arr_key, arr_flag


#0. Initialize the variables:
    json_balancer_stack = Stack()   # for the counter operation of the JSON elements.
    json_directive_stack = Stack()  # for validating the pairs positions.
    json_keys_stack = Stack()       # for column names of the new table.
    json_values_stack = Stack()     # for values of each column exists in the current JSON line.

    # The JSON counters:
    object_CTR = 0; array_CTR = 0;
    value_CTR = 1    #NOTE: because it only counts the delimiters ','.

    if not (table_no):#NOTE: important to accumulate old parsed JSON lines!!!
        tables_schema = [[] for _ in JSON_lines]    # lists of unique column names to avoid duplication
        tables_data = [[] for _ in JSON_lines]      # lists of values(even if lists) for each column name in the tables_schema
        unique_schema = []
    # ##from struct_json:

        k_arr_idx = -1 # for checking the 0 position of nested JSON objects

        arr_key = None                     ;   arr_flag = None
        #NOTE: they are FLAGS to decide the parsing whether to turn to normal list or list of objects(dictionaries)
       #arr_key: refers to the dicts       ,   arr_flag: refers to singular values
        
        val_arr = []# to combine the values of the normal list into one element during the parsing process, 
        #which in turn belongs to the same key.

        sub_object_CTR = 0
        sub_key_CTR = 0
    return ([json_balancer_stack, json_directive_stack, json_keys_stack , json_values_stack],    
        [tables_schema, tables_data, unique_schema], val_arr)

"""
As no user-defined nominal keys >>> PROTOTYPE  =) Message me if not! 'omar.negam@levelupesg.co'

____________________________ Outlines of the code:- 
1. read the lines.
2. statistics on number of blocks using symbol_stack.
[]. locate `:` of the pairs, for any further purpose (e.g., validation)
3-2. split into keys, values stacks.
3-1. filtering braces and commas.
4. collect unique(col_name), corresponding list of values for each.
4-2. refine the type for each column to its value in-place.
5. make all lists of values equal_len by `None` padding.
"""



def json_preview(line,json_balancer_stack,json_directive_stack):
    #declaration
    global object_CTR, array_CTR, value_CTR
    print(object_CTR)
    line = list(line)
    for index, token in enumerate(line):#Here is the counter engine starts up!
        #2. statistics on number of blocks using symbol_stack. 
            
        if token in ['{','[',',']:#TODOOO: " test cases
            json_balancer_stack.push(token)
            print("At push(with the positional index of the Last_In), openings are: ",json_balancer_stack.get(),index+1) 
        elif token == ':':
            json_directive_stack.push(index)

        if (token in ['}',']']) and ( json_balancer_stack.isNotEmpty()):
            #NOTE: printing current stats in a '\n' at the pop() stage.
            print("Before pop: ",json_balancer_stack.get(),'\n')#, current counts are: 
                
            while json_balancer_stack.peek() == ',':
                    value_CTR += 1
                    json_balancer_stack.pop()
            b = json_balancer_stack.pop()
            if token == '}' and b == '{':
                object_CTR += 1
            elif token == ']' and b == '[':
                array_CTR += 1
            else:
                print("Validation error!"); exit();

            print("After pop, the stack became: ",json_balancer_stack.get(),'\n')



        #///////////////    Here is the counter engine turns OFF!   \\\\\\\\\\\\\\\\\\\\


# for c in ['[',']','{','}',',']:
# line.remove(c)            #NOTE: but what about Map ?! =)  Here we go:-

    # 3-1. filtering braces and commas.
    mapped_lines = ''.join(list(map(lambda x: x+'\n' if x in ['[',']','{','}',','] else x,line)))# ['[',']','{','}',',']
# refined_line = list(filter(lambda x: len(x.strip()) > 1 or x == ' ',mapped_line.split('\n')))      DEPRECATED!


    colon_flag = 0           #NOTE: validation process of pairs positions
    margin = 0
    for i,v in enumerate(mapped_lines):
        # if mapped_lines[i] i
        if v == ':':#0 and colon_flag:
            
            print('actual_index: '
                ,i-margin, 'w.r.t predicted: ',json_directive_stack.get())
            colon_flag = i-margin in json_directive_stack.get()
            if not colon_flag:
                break
        elif v in ['[',']','{','}',',']:
            margin += 1

    return (mapped_lines, [object_CTR, value_CTR,  array_CTR], colon_flag)


def struct_json(mapped_lines,json_keys_stack, json_values_stack,val_arr=[]):
    #declaration
    global  value_CTR,sub_object_CTR,sub_key_CTR,arr_flag,arr_key,k_arr_idx

    # 3-2. split into keys, values stacks.
    for sub_way in mapped_lines[1:-2].split(','):
#'\n'.join(refined_line)

            #Hey, isn't the following a pipeline =) ?!
        sub_way = sub_way.replace('\n','').replace('{','')
                            # .replace('{','').replace('}','')
                                                            
            #NOTE: but for ], [ and :  >> they are used for the lists parsing

        pairs = sub_way.split('":',1)#NOTE: cAuTiOn, for misleading text, hold only on the 1st occurrence.
        k = False
        #NOTE: This is because the current `sub_way` may not contain the splitter ':'
        if len(pairs) > 1:
            k,v = pairs
        else:
            v = pairs[0] #NOTE: taking it as a normal string, because split() returns a list object.

    #TODO: intelli_type data refiner!!!
# type_refiner(k,v) #i.e. based on the key namespace

        if (v.find('[')                             +1):
            k += '[]'# All down this branching is initializing the nested array either of the 2 types.
            if (v.find('":')                             +1):
            #List of dictionaries
                k2,v = v.split('":')
                arr_flag = None
    # k = k#.replace('[','')
                arr_key = k.lstrip()#.replace('"','')
                k = k2.replace('[','')

#json_keys_stack.pop()
# k = (arr_key + '| ' + k.lstrip()).replace('[','')
# json_keys_stack.push(k.strip().replace('\n','').replace('[',''))

                k_arr_idx = json_keys_stack.get().index(json_keys_stack.peek()) +1
                print(v,"k_arr_idx: ",k_arr_idx)

            else:
                #List of values
                print("switching dict to arr.")
                # arr_key = None
                v = v.lstrip().replace("'",'')
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

        if arr_key:
            print("v_key:",v)
            if (v.find('}')+1):
                sub_object_CTR += 1
                print("subject: ",sub_object_CTR)
            # else:
            sub_key_CTR +=1
            print("subkey: ",sub_key_CTR)

        if v.find(']')                             +1:
                print("//]",v)
            #Close down ANY special parsing:                    
                b_key = []
                if arr_flag:#NOTE: for the last element, 
                        # like similar problems where the loop neglects the last elment right at the condition negativity*
                    v = ['<'] + val_arr + [v.replace("'",'')] + ['>']
                    # v[0] = '<'+str(v[0]);   v[-1] = str(v[-1]) + '>'
                    arr_len = len(v)
                    for item in v:
                        if ",'" in item:
                            arr_len += (item.split(','))

                    b_val = json_keys_stack.pop().replace('[]',f'[{arr_len-2}]')
                        #NOTE instead of slicing, then adding the length, because that key by any fault may NOT have the `[]`, so the function returns INTACT!
                    json_keys_stack.push(b_val.replace('"',''))
                    # sub_object_CTR = 0# This will ensure skipping the next for loop
                print("t",sub_key_CTR)
                for i in range(sub_object_CTR*sub_key_CTR*2):
                    b_key += [json_keys_stack.pop().replace('[]',f'[{sub_object_CTR};{sub_key_CTR};2]')]#NOTE: improved at October 25,2025
                       #NOTE instead of slicing, then adding the length, because that key by any fault may NOT have the `[]`, so the function returns INTACT!
                for b in b_key[::-1]:
                    json_keys_stack.push(b.replace('"',''))

                arr_key = None
                sub_object_CTR = 0

                

# json_values_stack.push()
                arr_flag = None
                val_arr = []
# continue
            
        




        if arr_flag:#NOTE: The accumulator of the list object.
#: was thought of just an extra assertion  ok?
            val_arr += [v.replace("'",'')]
            continue

        # 3-3. refine the type for each column to its value in-place.GOTO table_finalize
        # v = type_refiner(str(v).lstrip()
        #                                 .replace('\n','').replace('"','').replace('}','')
        #                                                                 .replace(']','').replace('[','')                                          
        #                 ,k)[0]#Native type validator.
        json_values_stack.push(str(v).lstrip()
                                        .replace('\n','').replace('"','').replace('}','')
                                                                        .replace(']','').replace('[','')
                                                                        )
            
# if '[' in list(v):
#     v += ']'     

# json_values_stack.push(v)# if (not arr_flag) else list(json_values_stack.pop())+[v])

    while json_values_stack.size() > value_CTR:
# print(json_values_stack.size())
        json_values_stack.pop();#NOTE: This for redundancy. ok?


def table_finalize(table_no, tables_schema, tables_data,unique_schema):
    #declaration
    global  json_keys_stack, json_values_stack

        #NOTE: Loading phase: with duplicates removal*
        # 4. collect unique(col_name), corresponding list of values for each.
    for element in json_keys_stack.get():
# [::-1]            
        if (not len(tables_schema[table_no])) or (element not in tables_schema[table_no]):
            tables_schema[table_no] += [element]
                # print(tables_schema[table_no][-1],element)
    for col in tables_schema[table_no]:
        if col not in unique_schema:
            unique_schema += [col]   #for series of JSON objects.     

        # for val in json_values_stack.get():
    for col in unique_schema:#tables_schema[table_no]:
        tables_data[table_no].append([type_refiner(json_values_stack.get()[i].strip(),k)[0] for i,k in enumerate(json_keys_stack.get()) if k == col])

    max_len = 0
        #5. make all lists of values equal_len by `None` padding.
    for sub_t in range(len(tables_data[table_no])):
        element = tables_data[table_no][sub_t]
        if len(element) > max_len:
            max_len = len(element)
        print("el",element)
        if "<" in str(element[0] if element else ''):
            print("el",element)
            tables_data[table_no][sub_t] = str(element[0])#.split('; ')

        #     for ted in range(sub_t):
        #     # while len(tables_data[table_no][sub_t]) < max_len:
        #         tables_data[table_no][ted] += [None]*max_len
        #             #NOTE: filling the empty lists or missing values with None*(max_len of the longest list)
        # else:
        #     max_len = len(element)
    tables_data[table_no] = [sub_t + [None]*(max_len-len(sub_t)) if len(sub_t) < max_len else sub_t for sub_t in tables_data[table_no]]

    dic = {k:v for k,v in zip(unique_schema,tables_data[0])}
    print(list(dic.keys()))
    print('_'*len(str(unique_schema)))
    for i in range(max_len):
        print([dic[k][i] for k in dic.keys()])
    # exit()
    return max_len,dic



#################################////////////////////////////////////#################################/////////////////////////#####################///////////
#From: 2nd year 'DataStructures' material... This is the backbone of the project
class Stack():
    """It is an Abstract Data Type with the transfer operation known as LIFO (or: First In Last Out)."""
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
"""
json_symbols = [('"',':',','),  #delimiters and modifiers
                    ('{','['),  #opening braces
                    ('}',']')   #closing braces
    ]
"""



def type_refiner(value,key=None):# A util func.
    """takes the singular item, whatever it is... except for the lists(they are guaranteed)
    ,   and validates its data type (e.g. removes punctuations from numerical items).
    * For the `key`, it is set BACK for future development to an intelligent validator based on the item keyword."""
    print(value)
    if "''" in value:
        return None, type([]).__name__ #Already sit in a list
        
    elif '<' in value:# October 23,2025
        
        # print("val",value[1:-1].split(', '))
        value = value.replace(",",';').split('; ')[1:-1]
        # print(value[0])
        ls_typ = type_refiner(value[0].replace("'",''),key)[1]
        # print(ls_typ);exit();
        return value,ls_typ

    elif not value.replace('.','').isnumeric():
        # print(value,"not numeric")
        for char in value:
            if char in [':','-']:
                print(value,"is date!!!!!!!!!!!")
                return value, 'date'

            elif char in [c for c in """1234567890!#$%&()*+,./;<=>?@\\^_`{|}~"""]:#abcdefghijklmnopqrstuvwxyz
                #NOTE: found this long string from: [string.ascii_lowercase + string.punctuation] \
                continue
                # return value, 'varchar'
            
            # else:
            #     print(value,"is char!!!!!!!!!!!")
            #     return value, 'char'
            print(value,"is VARchar!!!!!!!!!!!")
            return value, 'varchar'

    else:
        if '.' in value:
            value = float(value)
            return value, type(value).__name__
        else:
            value = int(value)
            return value, type(value).__name__
        print(value,"is numeric!!!!!!!!!!!")
# print('\n\n\n\n\n',k,'\n\n\n\n\n\n')
    # return value,k


#1. Initialization of stats, and marshals: in the main_init point.


if __name__ == "__main__":
    with open(input("src_filename: "),'r') as file:# The main header
        # 1. read the lines.

        JSON_lines = list(filter(lambda x: x.find('{"') in [0,1]
            ,file.readlines()))#NOTE: searches alooooooooooooooong^ the file for JSON values.
        

    for table_no, line in enumerate(list(map(lambda x: x.replace('\n','')#.split(' ',1)[-1].lstrip() 
                                                                        #NOTE: this is file-specific operation
        #                                   So, it is recommended to have me any thing stripped out surrounding the JSON part.
                                            ,JSON_lines))):

    #2. Initialization of stats, and marshals: in the main_init point.
        stacks,sets,val_arr = main_init(table_no)

        #NOTE: table_no, for the logging and the unique lists.
        mapped_lines,ls_ctr,flags =  json_preview(line,*stacks[:2])


        print('\n\nFinal stats of the json content (total_n(objects), n(pairs), total_n(arrays)):\n', ls_ctr)
        input(f"######## : INDEXES ARE {flags}! #######\n Press `Enter` or `Ctrl+c` accordingly:");

        struct_json(mapped_lines,*stacks[2:4],val_arr)

        print('\n\n First look at the ETed table: _duplicates exist_*\n\n')
        print((json_keys_stack.get()),'\n', json_values_stack.get())
        print('First stats: ', json_keys_stack.size(), json_values_stack.size())


        max_len,dic = table_finalize(table_no, *sets)
    #     print('\n\n',f"tables_schema ({len(tables_schema[table_no])}): ",tables_schema[table_no])
    #     print('\n\n',f"tables_data ({len(tables_data[table_no])*max_len}) {max_len} item(s)/key: ",tables_data[table_no])
    #     print('\n__________\n',f"End of JSON record: {table_no}!",'\n__________\n')

    # print(tables_schema,[len(i) for i in tables_schema], len(unique_schema))
    # print((unique_schema))
    # print([len(i) for i in tables_data],tables_data)

# October 26    , 2025
    with open(input("dst_filename: "),'w') as file:# The main header

        # file.write(', '.join(list(dic.keys())))#str(map(lambda x: x,list(dic.keys())))
        file.write(', '.join(unique_schema))
        file.write('\n')
        for i in tables_data:
            # file.write(', '.join([str(dic[k][i]) for k in dic.keys()]))
            for elmnt in i:
                file.write(',,,,,,,,,,,,,, '.join([str(mnt) for mnt in elmnt]))
            file.write('\n')
# November 4, 2025

    print("\\\\\\ FIRST SAMPLE #######")
    print(list(dic.keys()))
    print('_'*len(str(unique_schema)))
    for i in range(max_len):
        print([dic[k][i] for k in dic.keys()])
    # exit()



"""A sample to try on:
{"section": "Environmental and Social Management System (ESMS)", "score": 4.47, "target": 5.0, "gap": 0.53, "actions": ["Standardize documentation and reporting formats across departments.", "Integrate ESG considerations into enterprise management systems.", "Engage third parties for evaluations or certifications.", "Embed ESG KPIs into strategic planning processes.", "Publish sustainability or impact reports with stakeholder input."]}

Have fun!
"""


# `jp` shell command .......... TBC
# TODO: _Use Shell Scripts to Increase Portability_
# -------------------------------------------------------------------

#  
