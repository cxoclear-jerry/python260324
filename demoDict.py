# demoDict.py

# type casting
a = {1, 2, 3}
b = tuple (a)
print (b)
c = list (b)
c.append (4)
print (c)

# dictionary type example
color = {'apple':'red', 'banana':'yellow'}
print (color)
print (len(color))
color ['cherry'] = 'purple'
print (color)
print (color['apple'])
del color['apple']
print (color)
for item in color.items():
    print (item)