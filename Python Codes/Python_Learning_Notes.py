# 使用方法修改字符串的大小写
test_1="I Love The University of Hong Kong"
print (test_1.title())
print (test_1.upper())
print (test_1.lower())
#合并(拼接)字符串
first_name = "Andrew" 
last_name = "YU" 
full_name = first_name + " " + last_name
#字符串可以简单地用"+"来连接，这种合并字符串的方法称为拼接

# f-string 格式化输出
print(f"{first_name} {last_name}")  # 使用f-string格式化输出名字和姓氏
# 语法,含义,示例
# :.2f,保留两位小数,"f""{3.14159:.2f}"" -> 3.14"
# :0>3d,左侧补零凑足3位,"f""{5:0>3d}"" -> 005"
# ":,",千分位分隔符,"f""{1000000:,}"" -> 1,000,000"
# :.1%,百分比格式,"f""{0.856:.1%}"" -> 85.6%"

print (full_name)
# 删除空白
# Python能够找出字符串开头和末尾多余的空白。
# 要确保字符串末尾没有空白,可使用方法  rstrip()。
# 类似的，如果要确保字符串开头没有空白，可使用方法.lstrip()
# 如果要同时剔除字符串两端的空白，可使用方法.strip()
test_for_strip="  I am a Chinese   "
print (test_for_strip.rstrip())
print (test_for_strip.lstrip())
print (test_for_strip.strip())
# 通过这三种方式删除空白的方法都是暂时的，如果要彻底改变，要对变量重新赋值
test_for_strip=test_for_strip.strip()
test_for_strip_2=test_for_strip+"I love my country."
print (test_for_strip_2)

# python算术运算符优先级与括号
#'+' '-' '*' '/'加减乘除    '**'-幂运算    '//'-整除运算    '%'-取模运算
# 和数学中的“先乘除后加减”一致，Python 也有严格的执行顺序：
# 括号 ()：拥有最高优先级，任何需要先算的都加括号。
# 幂运算 **：第二优先级。
# 乘、除、整除、取模 *, /, //, %：同一级别，从左往右算。
# 加、减 +, -：最低优先级。
result = (5 + 3) * 2 ** 2 / 4
# 计算顺序：
# 1. 括号内: 5 + 3 = 8
# 2. 幂运算: 2 ** 2 = 4
# 3. 乘除从左往右: 8 * 4 = 32, 然后 32 / 4 = 8.0
print(result) # 输出 8.0
print(f"{result:.6f}") #  使用f-string格式化输出结果，保留6位小数

#数据输出格式拓充
#格式代码,说明,示例 (x = 1.23),结果
# {x:.2f},固定 2 位小数,    f"{x:.2f}",1.23
# {x:+.2f},显示正负号,  f"{x:+.2f}",+1.23
# {x:10.2f},总宽 10，右对齐,    f"{x:10.2f}",      1.23
# {x:010.2f},总宽 10，补零, f"{x:010.2f}",0000001.23
# {x:.0f},不保留小数（取整）,   f"{x:.0f}",1
# {x:.1%},百分比格式,   f"{0.123:.1%}",12.3%

#关于进制更改
# 字母,进制,示例 (x = 42),输出结果
# b,二进制 (Binary),    f"{x:b}",101010
# o,八进制 (Octal),     f"{x:o}",52
# x,十六进制 (Hex),"    f"{x:x}",2a (小写)
# X,十六进制 (Hex),"    f"{x:X}",2A (大写)
# d,十进制 (Decimal),"  f"{x:d}",42 (默认值)
test_x = 42
print(f"{test_x:X}") #  打印test_x的十六进制大写形式
print(f"{test_x:x}") #  打印test_x的十六进制小写形式

# 使用函数 str()避免类型错误
#在 Python 中，str() 是最常用的内置函数之一。
# 它的核心作用是：将其他数据类型（数字、列表、字典、对象等）转换成字符串（string）类型。
age_1=20
string_1=first_name+" "+last_name+" is "+str(age_1)+" years old."#利用str将age_1转换为字符串类型
print (string_1)

    #列表
#列表由一系列按特定顺序排列的元素组成。
#可以将任何东西加入列表中
#在Python中,用方括号([])来表示列表,并用逗号来分隔其中的元素。
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles)
#要访问列表的任何元素,只需将该元素的位置或索引告诉Python即可。 
#要访问列表元素,可指出列表的名称,再指出元素的索引,并将其放在方括号内。
print (bicycles[0])
print (bicycles[0].title())

# 索引从 0 而不是 1 开始
# Python为访问最后一个列表元素提供了一种特殊语法。
# 通过将索引指定为-1,可让Python返回最后一个列表元素
# 这种约定也适用于其他负数索引。
# 例如,索引-2返回倒数第二个列表元素, 
# 索引-3返回倒数第三个列表元素,以此类推。

        #修改，添加和删除列表中的元素


            #? 修改列表元素：

# 修改列表元素的语法与访问列表元素的语法类似。
# 要修改列表元素,可指定列表名和要修改的元素的索引,再指定该元素的新值。
motorcycles = ['honda', 'yamaha', 'suzuki'] 
print(motorcycles) 
motorcycles[0] = 'ducati' 
print(motorcycles)
#直接找到要修改的位置，重新赋值。

            #? 在列表中添加元素
# 1. 在列表末尾添加元素  .append()
# 2. 在列表中插入元素   .insert(0,'ducati')

# append 函数
motorcycles.append("Ducati")
#append将元素添加到列表末尾。

#insert函数
motorcycles.insert(4,'BMW')
#.insert 后面括号里用逗号间隔，
# 逗号前面写要放置新元素的索引，后面写要添加的元素
#其余未被修改元素自动保持不动或者索引后移，不必考虑。

            #? 从列表中删除元素

# 1. 使用del语句删除元素
del motorcycles[1]
print(motorcycles)

# 2. 使用方法pop()删除元素
#.pop()里面如果留空，默认弹出列表最后一个元素
popped_motorcycle = motorcycles.pop() 
print(motorcycles) 
print(popped_motorcycle)

# 3. 弹出列表中任何位置处的元素

# 实际上,你可以使用pop()来删除列表中任何位置的元素,
# 只需在括号中指定要删除的元素的索引即可。
first_owned = motorcycles.pop(0) 
print('The first motorcycle I owned was a ' + first_owned.title() + '.')

# 4. 根据值删除元素

#有时候,你不知道要从列表中删除的值所处的位置。
# 如果你只知道要删除的元素的值,可使用方法remove()。
motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
print(motorcycles)  
motorcycles.remove('ducati') 
print(motorcycles)
motorcycles.remove('yamaha') 
print(motorcycles)

# 组织列表
#使用方法 sort()对列表进行永久性排序
cars = ['bmw', 'audi', 'toyota', 'subaru'] 
cars.sort() 
print(cars)
#可以按照与字母顺序相反的顺序排列列表元素
#只需要在sort（）括号里传递参数"reverse=True"
cars.sort(reverse=True)
print (cars)

# 使用函数 sorted()对列表进行临时排序
# 要保留列表元素原来的排列顺序,同时以特定的顺序呈现它们,
# 可使用函数sorted()。
# 函数 sorted()让你能够按特定顺序显示列表元素,
# 同时不影响它们在列表中的原始排列顺序

cars = ['bmw', 'audi', 'toyota', 'subaru'] 
print("Here is the original list:") 
print(cars)  
print("\nHere is the sorted list:") 
print(sorted(cars))  
print("\nHere is the original list again:")
print(cars)
print("\nHere is the reversed list")
print (sorted(cars,reverse=True))

#用函数len确定列表的长度
cars = ['bmw', 'audi', 'toyota', 'subaru']  #  创建一个包含多个汽车品牌的列表
print(len(cars)) #  使用len()函数获取列表中的元素数量，并打印结果

#操作列表

# for循环
magicians = ['alice', 'david', 'carolina'] 
for magician in magicians:#for 循环后面一定要加上':'
    print(magician)#for 循环下面的语句缩进表示语句在这个循环里，执行多次
# 编写for循环时,对于用于存储列表中每个值的临时变量,可指定任何名称
# 在for循环后面,没有缩进的代码都只执行一次,而不会重复执行。
#! python 里面的缩进不是随便的，通常与循环有关，避免不必要的缩进

#函数 range()
for value in range(1,5):
    print(value)
 # 上述代码好像应该打印数字1~5,但实际上它不会打印数字5:
# 函数range()让Python从你指定的第一个值开始数,
# 并在到达你指定的第二个值后停止,因此输出不包含第二个值(这里为5)。

# 使用函数range()时,还可指定步长
#range 函数括号里面（a,b,c）,
# a表示起点（包含），b表示终点（不含)，c表示步长，
# 步长就是连续两个数之间的差值

for value in range (1,100,2): #  使用for循环遍历1到100之间的奇数 range(1,100,2)生成一个从1开始，到100结束（不包括100），步长为2的数字序列

    print (value) #  打印当前遍历到的奇数值
    
# 简单的统计计算函数
# sum   min   max三个函数可做简单统计
#如sum(digits),min(digits)
digits=list(range(1,100,2)) 
# 使用range函数生成一个从1到100（不包括100），步长为2的数字序列
# 然后将这个序列转换为列表并赋值给变量digits
#列表名=list（range（a,b,c））

print(sum(digits))

# 列表解析
squares = [value**2 for value in range(1,11)] 
print(squares)

#与上面digits定义等价的是 digits=[i for i in range(1,100,2)]
# 要使用这种语法,首先指定一个描述性的列表名,如squares;

# 然后,指定一个左方括号, 并定义一个表达式,用于生成你要存储到列表中的值。
# 在这个示例中,表达式为value**2,它计算平方值。
# 接下来,编写一个for循环,用于给表达式提供值,再加上右方括号。
# 在这个示例中,  for循环为for value in range(1,11),它将值1~10提供给表达式value**2。
# 请注意,这里的for 语句末尾没有冒号

#使用列表的一部分（切片）

# 要创建切片,可指定要使用的第一个元素和最后一个元素的索引。
# 与函数range()一样,Python切片在到达你指定的第二个索引前面的元素后停止。
# 要输出列表中的前三个元素,需要指定索引0~3, 这将输出分别为0、1和2的元素。
players = ['charles', 'martina', 'michael', 'florence', 'eli']  #  创建一个包含球员名字的列表
print(players[0:3]) #  使用切片操作打印列表中的前三个元素
#  切片的规则：
# （1），若切片冒号两侧都有数值，并且冒号左侧数值是不小于0的数字，
#        切片将从冒号左侧数字的索引开始（包含），到冒号右侧数字的索引结束（不含）

#  (2)，若切片冒号左侧无数值，将自动默认从第一个索引开始，到冒号右侧索引结束（不含）
#       也就是说，若冒号左侧无数值，[:a]等价于[0:a]

#  (3), 若切片右侧无数值，意思是从左侧索引开始，到列表最后一个元素结束


# （4), 若切片左侧数值是一个负数，与之前的列表里负数含义一致，-1就是倒数第一个，-2就是倒数第二个
#       players[-3:]就表示最后三个元素
#       players[-5:-2]表示从倒数第五个元素到倒数第三个元素（不含倒数第二个）
#       切片的左含右不含原则是一直适用的，除了冒号两侧缺数值的情况。

# （5），切片冒号两侧全是空的，表示对列表整体的切片。
#?   players[:]等价于players.copy()

# 遍历切片
players = ['charles', 'martina', 'michael', 'florence', 'eli']  
print("Here are the first three players on my team:")
for player in players[:3]: 
    print(player.title())
    
#复制列表
my_foods = ['pizza', 'falafel', 'carrot cake'] 
friend_foods = my_foods[:]  
print("My favorite foods are:") 
print(my_foods)  
print("\nMy friend's favorite foods are:") 
print(friend_foods)
#如果只是想复制列表里面的元素，不与源列表建立关联，就用切片

my_foods = ['pizza', 'falafel', 'carrot cake']  #  创建一个包含我最喜欢的食物的列表
friend_foods = my_foods[:]  
my_foods.append('cannoli')  
friend_foods.append('ice cream')  
print("My favorite foods are:") 
print(my_foods)  
print("\nMy friend's favorite foods are:") 
print(friend_foods)

#输出结果可以看见两个列表元素不同

my_foods = ['pizza', 'falafel', 'carrot cake']  #这行不通  
friend_foods = my_foods  
my_foods.append('cannoli') 
friend_foods.append('ice cream')  
print("My favorite foods are:") 
print(my_foods) 
print("\nMy friend's favorite foods are:") 
print(friend_foods)
#打印结果可以发现两个列表元素完全一致
#实际上进行了赋值操作
#它们操作的是同一个内存地址

