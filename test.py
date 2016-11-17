import io


def hex_to_bytes(hex_str):
    bytes = []
    hex_str = ''.join(hex_str.split(' '))

    for i in range(0, len(hex_str), 2):
        bytes.append(int(hex_str[i:i + 2], 16))
    return bytes


def byte_gen(stream):

    while True:
        a = stream.read(1)
        if a == '':
            raise StopIteration
        yield bytearray(a)[0]


# print hex_to_bytes('01000204')

barr = bytearray.fromhex('01000204')
stream = io.BytesIO(barr)
g = byte_gen(stream)

'''
print next(g)
print next(g)
print next(g)
print next(g)
print next(g)
'''
for b in byte_gen(stream):
    print ':', b

'''
with io.open('komm.twkb', 'rb') as stream:
    for b in byte_gen(stream):
        print ':', b
'''

#print bytearray(stream.read(1))[0]
#for b in stream:
#    data = bytearray(b)
#    print data[0]

'''
raw_bytes = stream.getvalue()
print(len(raw_bytes))
print(type(raw_bytes))
'''
'''
print barr

print type(barr)
for c in barr:
    print c

stream = io.BytesIO(barr)

print type(stream.getvalue())

for d in stream.getvalue():
    print type(d)
'''

#print len(bytes('01000204'))
#for b in bytearray.fromhex('01000204'):
#    print b
