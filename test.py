from twkbpy import decode
import io

with io.open('komm.twkb', 'rb') as stream:
    decode(stream)
