# 元组
from collections import namedtuple

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delphi NCR', 'IN', 21.935, (28.61388, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.43333, -99.1333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))


# namedtuple(className, Fieldnames)
City = namedtuple('City', 'name country population coordinates')

tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))

print(tokyo)

s = 'bicycle'

print(s[::3], s[::-1])


resp = ['0x111', '0x5522', '0x122']

print(resp[::-1])


def factorial(n):
    return 1 if n < 2 else n * factorial(n-1)

# 4 * 3 * 2 * 1
print(factorial(4)) 