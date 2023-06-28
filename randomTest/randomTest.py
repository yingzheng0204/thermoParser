# import io

# f = open('test')
# print(type(f))

# if type(f) is io.TextIOWrapper:
# 	print('y')

f = open('test')
print(f.readline())
print(f.readline() == '\n')
print(f.readline() == '')
