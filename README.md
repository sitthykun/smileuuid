# Smile Uuid v0.1.0
The primary concept is to replace UUID strings with numeric values in Python 3.x.

Ex1:\
Create an instance with the exist key
```
smile = SmileUuid('a-cde-dce')

print(f'current id: {smile.currentId()}')
print(f'next id: {smile.nextId()}')
print(f'save file is {smile.saveCache()}')
```
output:
```
current id: 123456789012352
next id: 123456789012353
save file is 1
```

Ex2: \
Create an instance with the exist key or not exist\
that will use the default value and starts with 100000000000000 (100,000,000,000,000)
```
smile = SmileUuid(isForceOverrideNewId= False, startId= 123456789012347, key= 'a-cde-dce')

print(f'current id: {smile.currentId()}')
print(f'next id: {smile.nextId()}')
print(f'save file is {smile.saveCache()}')
```
output:
```
current id: 100000000000000
next id: 100000000000001
save file is 1
```

Ex3:\
Create an instance with the exist key or not exist\
with overriding or starting with 123456789012347
```
smile = SmileUuid(isForceOverrideNewId= True, startId= 123456789012347, key= 'a-cde-dce')

print(f'current id: {smile.currentId()}')
print(f'next id: {smile.nextId()}')
print(f'save file is {smile.saveCache()}')
```
output:
```
current id: 123456789012347
next id: 123456789012348
save file is 1
```

Ex4:\
Enable redis\
it has to set two place;\
1. enableRedis= True
2. smile.configRedis(host= '127.0.0.1', port= 6379, index= 0, password= '123456')
```
smile = SmileUuid(key= 'a-cde-dce', enableRedis= True)
print('load redid config is ', smile.configRedis(host= '127.0.0.1', port= 6379, index= 0, password= '123456789'))
print(f'current id: {smile.currentId()}')
print(f'next id: {smile.nextId()}')
print(f'save file is {smile.saveCache()}')
```
output:
```
current id: 123456789012347
next id: 123456789012348
save file is 1
```

Ex5:\
Set cachePath\
it will set absolute location by following\
the below cachePath and key will be generated like this "miss-mon/cache/cbf5ff5ce981810033f3f0e06d687c1a"
```
smile = SmileUuid(cachePath= 'miss-mom', key= 'a-cde-dce', enableRedis= True)
print(f'current id: {smile.currentId()}')
print(f'next id: {smile.nextId()}')
print(f'save file is {smile.saveCache()}')
```
output:
```
current id: 123456789012347
next id: 123456789012348
save file is 1
```
