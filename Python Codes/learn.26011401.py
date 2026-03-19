# # 修复变量命名规范，统一小写+下划线
# message = "ShangHaiJiaoTongUniversity" #  定义一个字符串变量，存储上海交通大学的英文名称
# string_1 = 'I Love You'
# favourite_language = "  Python   "
# # 修复：lstrip()+rstrip()合并为strip()，并赋值生效
# #strip
# favourite_language = favourite_language.lstrip()  #  使用lstrip()方法去除变量favourite_language中字符串左侧的空白字符
# print(favourite_language)  # 现在输出：Python

# # 修复：拼接时添加空格分隔，提升可读性
# full_name = f"{message} {string_1}"
# print(message.title())  # 输出：Shanghaijiaotonguniversity（首字母大写）
# print(message.upper())  # 输出：SHANGHAIJIAOTONGUNIVERSITY
# print(message.lower())  # 输出：shanghaijiaotonguniversity
# print(string_1)         # 输出：I Love You
# print(full_name)        # 输出：ShangHaiJiaoTongUniversity I Love You
# # 修复：换行符后添加空格，格式更美观
# print(f"Hello\n {full_name.title()}")

# # 修复：f-string引号冲突（改用单引号包裹外层，内部直接用双引号，无需转义）

# # 定义一个变量name，并赋值为字符串"Albert Einstein"
# name = "Albert Einstein"  # 存储著名物理学家阿尔伯特·爱因斯坦的全名
# age = 70
# # 定义一个字符串变量，存储地址信息
# address = "Princeton University"  # 将普林斯顿大学的地址赋值给address变量
# print(f"{name} once said, \"A person who never made a mistake never tried anything new.\"")

# # 数值运算（无问题，保留）
# print(3**5)  # 输出：243
# print(5//2)  #  这是一个整数除法的示例，计算5除以2的商
# print(100_200_300_400_500_600_700_800_900)  # 输出：100200300400500600700800900

# # 多变量赋值（无问题，保留）
# x, y, z = 1, 2, 3
# print(x, y, z)  # 输出：1 2 3



# bicycles = ['xds', 'GIANT', 'Phoenix', 'FOREVER', 'JAVA', 'TREK']
# print(bicycles[0].upper())  # 输出：XDS
# print(bicycles[-1].lower())  # 输出：trek
# print(f"My favourite bicycle is {bicycles[-2].upper()}")  # 输出：My favourite bicycle is JAVA

# bicycles.insert(1, 'PHILIP')
# bicycles.insert(2,"YAO_YU")
# bicycles.append('YAMAHA')
# # del bicycles[1]
# print(bicycles)  # 输出：['xds', 'GIANT', 'Phoenix', 'FOREVER', 'JAVA', 'TREK', 'YAMAHA']

# bicycles_pop = bicycles.pop(5)
# print(bicycles_pop)  # 输出：GIANT
# print(bicycles)      # 输出：['xds', 'Phoenix', 'FOREVER', 'JAVA', 'TREK', 'YAMAHA']

# cars = ['audi', 'bmw', 'benz', 'toyota']
# # 对cars列表进行排序操作
# # sort()方法会直接对原列表进行升序排序，不创建新的列表
# # 排序后的列表元素将按照从小到大的顺序重新排列
# cars.sort()
# print(cars)  # 输出：['audi', 'benz', 'bmw', 'toyota']
# print(sorted(cars, reverse=True))  # 输出：['toyota', 'bmw', 'benz', 'audi']
# print(cars)  # 输出：['audi', 'benz', 'bmw', 'toyota']（sort()是永久排序，sorted是临时）

# cars.insert(3, 'lamborghini')
# print(cars)

# cars.append('ANDY')
# print(cars)
# cars.reverse()
# print(cars) 
# print(len(cars))  
# # cars.reverse()
# # 循环遍历（无问题，保留）
# for car in cars:
#     print(car)
#     print(f"I want to drive {car}\n")
# print("thank you for your efforts")

# # # 数值循环（修复：print后去掉多余空格，符合PEP8）
# for i in range(1, 10):
#     print(i) 

# numbers=list(range(1,10,2))
# print(numbers)

squares=[]
for num in range(1,11):
    squares.append(num**3)  

print(squares)
print(min(squares))
print(max(squares))
print(sum(squares))

# # data_1=[date**5 for date in range(1,100,5)]
# # print (data_1)

# data_2=[dare+1 for dare in range(1,100_000_00)]
# print (sum(data_2))

# from datetime import datetime
# now = datetime.now()    # 获取当前时间
# print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 格式化时间（2026-01-14 10:00:00）
# # 注释的列表操作（取消注释可运行）
# # bicycles.remove('Phoenix')
# # print(bicycles)

# # 多行f-string（无问题，保留）
# # info = f
# # 用户信息：
# # 姓名：{name}
# # 年龄：{age}
# # 地址：{address}
# players=['james','curry','kobe','wade','Leborn','Messi'] #  定义一个包含多个球员名字的列表players

# # 打印players列表的前三个元素（索引0、1、2）
# print(players[0:3]) #  使用切片操作获取列表中从索引0开始到3但不包含3的元素

# print(players[1:4]) #  打印players列表中索引为1到3的元素（切片操作，不包含索引4）
# # 打印players列表中的前6个元素
# print(players[:6])    # 使用切片操作获取从索引0开始到索引6（不包含6）的所有元素
# # 打印players列表中的最后两个元素

# print(players[2:])  # 打印players列表中从第三个元素开始到末尾的所有元素
# print(players[-2:]) #  打印players列表中最后两个元素 使用切片操作[-2:]获取从倒数第二个元素到列表末尾的所有元素
# # for player in players: #  遍历players列表中的每个玩家
# #     print(player.title()) #  打印每个玩家的名字，并使用title()方法将首字母大写
# my_favourite_players=players[-3:]
# print("Below are my favourite players\n")
# print(my_favourite_players) #  打印我最喜欢的球员名单
print("我是帅哥")




'''
// 将键绑定放在此文件中以覆盖默认值
[    //copilot 代码预测开启与关闭
    {
        "key": "ctrl+alt+p",      // 设置触发键（可自定义）
        "command": "editor.action.inlineSuggest.trigger", // 触发预测命令
        "when": "editorTextFocus && !inlineSuggestionVisible" 
    },
    {
        "key": "ctrl+alt+p",      // 同一按键用于关闭
        "command": "editor.action.inlineSuggest.hide",
        "when": "inlineSuggestionVisible" 
    },
    {
        "key": "ctrl+f6",
        "command": "python.execInTerminal-icon"
    },
    {
        "key": "f6",
        "command": "-workbench.action.focusNextPart"
    },
    {
        "key": "ctrl+p",
        "command": "codegeex.askcodegeex.comment"
    },
    {
        "key": "tab",
        "command": "editor.action.inlineSuggest.commit",
        "when": "editorFocus && inlineSuggestionHasIndentationLessThanTabSize && inlineSuggestionVisible && !editorHoverFocused && !editorReadonly && !editorTabMovesFocus"
    },
    {
        "key": "tab",
        "command": "-editor.action.inlineSuggest.commit",
        "when": "editorFocus && inlineSuggestionHasIndentationLessThanTabSize && inlineSuggestionVisible && !editorHoverFocused && !editorReadonly && !editorTabMovesFocus"
    },
    {
        "key": "tab",
        "command": "editor.action.inlineSuggest.commitAlternativeAction",
        "when": "inInlineEditsPreviewEditor"
    },
    {
        "key": "shift+tab",
        "command": "-editor.action.inlineSuggest.commitAlternativeAction",
        "when": "inInlineEditsPreviewEditor"
    }
    
]'''