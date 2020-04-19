import json
from sortedcontainers import SortedDict
from datetime import datetime, timedelta
cache = {"dummy" : [datetime.now(), "23"]}
sortedset = {}

#method for GET command....fetching from cache dictionary
def get_value(key):
    if key in cache:
        return cache[key][1]
    else:
        return "nil"

#setting value corrosponding to key
def set_value(key, value):
    list = [-1, value]
    cache[key] = list
    return "OK"

#inseting new value in sorted set
def add_set(key,score,value):
    if key in sortedset:
        sortedset[key][score] = value
        print(sortedset[key][score])
    else:
        temp = SortedDict()
        temp[score] = value
        sortedset[key] = temp
    return "OK"

def get_set():
    items = {}
    for key in list(sortedset):
        items[key] = sortedset[key]
    return items

#setting expiry for perticular key in cache
def set_expiry(key,time):
    if key in cache:
        print(cache[key][0])
        cache[key][0] = datetime.now() + timedelta(seconds = int(time))
        print(cache[key][0])
        return "1"
    else:
        return "0"

#finding element in given range for perticular key
def range_elements(key,left,right):
    dict = sortedset[key]
    items = dict.items()
    left = int(left)
    right = int(right)

    if left < 0:
        left = len(items) - (-1 * left)
    if right < 0:
        right = len(items) - (-1 * right)

    lower = min(left,right)
    upper = max(left,right)

    print(items[lower:upper+1])
    return "OK"

def rank(key,value):
    pivot = 0
    list = sortedset[key].values()

    for i in list:
        if(i == value):
            return str(pivot)
        else:
            pivot = pivot + 1
    return "-1"

#removing expired key-value from our cache
def remove_expired():
    for key in list(cache):
        if cache[key]!=-1 and cache[key][0]<datetime.now():
            del cache[key]

#saving all over cache data to a file for persistancy
def save():
    with open('cache.txt', 'w') as outfile:
        json.dump(cache, outfile)
    with open('set.txt', 'w') as outfile:
        json.dump(sortedset, outfile)
    return "OK"

#loading cache data from our storage when server restarts
def onstart():
    with open('cache.txt') as json_file:
        cache = json.load(json_file)
    with open('set.txt') as json_file:
        sortedset = json.load(json_file)
    return "OK"

#task method run in 60 seconnds interval to remove expired cache and take backup of our cache
def task():
    remove_expired()
    save()
    print("I am running tsk1 at ", datetime.now())
    return "OK"
