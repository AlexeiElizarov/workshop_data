class OopsExcepion(Exception):
    pass

def a(a, b):
    if b == 0:
        raise OopsExcepion(b)
    return a / b

try:
    a(1, 0)
except Exception as other:
    print('Exception:', other)
except OopsExcepion as oops:
    print(oops)

