import json
from heapq import heappush, heappop
from sortedcontainers import SortedDict
from datetime import datetime, timedelta
cache = {}
set = {}
lookup = {}

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

    if value in lookup and key in lookup[value]:
        list = set[key]
        previous_score = lookup[value][key]
        list.pop(previous_score,-1)
        set[key] = list

    if key in set:
        dict = set[key]
        if score in dict.keys():
            heappush(dict[score],value)
        else:
            temp = []
            heappush(temp,value)
            dict[score] = temp
        set[key] = dict
    else:
        temp = SortedDict()
        temp[score] = []
        heappush(temp[score],value)
        set[key] = temp

    lookup[value] = {key : score}
    return "OK"

def get_set():
    items = {}
    for key in list(set):
        items[key] = set[key]
    return items

#setting expiry for perticular key in cache
def set_expiry(key,time):
    if key in cache:
        cache[key][0] = datetime.now() + timedelta(seconds = int(time))
        return "1"
    else:
        return "0"

#finding element in given range for perticular key
def range_elements(key,left,right):
    items = []
    for i in set[key].values():
        items = items + list(i)

    left = int(left)
    right = int(right)

    if left < 0:
        left = len(items) - (-1 * left)
    if right < 0:
        right = len(items) - (-1 * right)

    lower = min(left,right)
    upper = max(left,right)

    ans = {"values:" : items[lower:upper+1]}
    return ans

def rank(key,value):
    pivot = 0
    list = []
    for i in set[key].values():
        list = list + i

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
        json.dump(set, outfile)
    with open('lookup.txt', 'w') as outfile:
        json.dump(lookup, outfile)
    return "OK"

#loading cache data from our storage when server restarts
def onstart():
    with open('cache.txt') as json_file:
        cache = json.load(json_file)
    with open('set.txt') as json_file:
        set = json.load(json_file)
    with open('lookup.txt') as json_file:
        lookup = json.load(json_file)
    return "OK"

#task method run in 60 seconnds interval to remove expired cache and take backup of our cache
def task():
    remove_expired()
    save()
    return "OK"
