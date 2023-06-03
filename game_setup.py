# diviz =[]
# x = 16
# for i in range(50):
#     multiple = i * x
#     if multiple % 16 == 0:
#         b = multiple // x
#         diviz.append((multiple, b))
         
        
# print(diviz)
# 256 x 256 = 16 blocks of 16 x 16 blocks of 16

diviz =[]
x = 28
for i in range(19):
    multiple = i * x
    if multiple % 28 == 0:

        diviz.append((i, multiple))
print(diviz)