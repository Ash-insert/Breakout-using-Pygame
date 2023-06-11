import random

Width = 800
Height = 600
Scale_Fac = (Width - 3 * 7)/(384 * 8) #for scaling blocks
Top_Offset = 25  #top offset for blocks
Block_Offset = 3  #Horizontal block offset
Block_Size = [Scale_Fac*384, Scale_Fac*128] 
Ball_Radius = 0.1 * 128
Heart_Scale = 0.15

Block_Type = { 2 : '01', 1 : '02', 4 : '03', 3 : '04', 6 : '05', 5 :'06', 8 : '07', 7 : '08', 10 : '09', 9 : '10' , 
              12 : '11', 11 : '12',  14 : '13', 13 : '14', 16 : '15', 15 : '16', 18 : '17', 17 : '18',  20 : '19', 19 : '20'}

Upgrade_Type = { 'slow' : 41, 'fast' : 42, 'laser' : 53, 'heart' : 60}

#creating a shape for block display
Shape = []
for i in range(5):
    l_1 = []
    l_2 = []
    for j in range(10):
        l_1.append(5 - i)
        l_2.append(5 - i)
    Shape.append(l_1)
    Shape.append(l_2)

#adding random blocks of different colors in each row
for i in range(5):
    Shape[2*i+1][random.randint(0,7)] = 5 + (5- i)


