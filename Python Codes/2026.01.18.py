# squares=[value**2 for value in range(1,110,10)] #  使用列表推导式生成一个平方数列表 从1开始，每次增加10，直到109为止，计算每个值的平方
# if (121 in squares): #  检查121是否在平方数列表中
#     print("YAO") #  如果121在列表中，则打印"YAO"
# request_toppings=['mushrooms','green peppers','extra cheese']
# for request_topping in request_toppings:
#     print(f"Adding {request_topping}")
# print("\n\tFinished making your pizza")
# users=['admin','lin','Yu','wu','Yao']
# for user in users:
#     if user=='Yao':
#         print(f"Hello {user},would you like to see a status report?")
#     else:
#         print(f"Hello {user},thank you for logging again")
# alien_0={'color':'blue','points':5}
# print(alien_0['color'])
# print(alien_0['points'])
# alien_0['x_position']=0
# alien_0['y_position']=25
# print (alien_0)   

# alien_0={'color':'green'}
# print (f"The alien_0 is {alien_0['color']}")
# alien_0['color']='pink'
# print (f"The alien_0 now is {alien_0['color']}")

alien_0={'x_position':0,'y_position':25,'speed':'fast','points':99}
print (f"origional position:{alien_0['x_position'],alien_0['y_position']}")
if alien_0['speed']=='slow':
    x_increment=1
elif alien_0['speed']=='medium':
    x_increment=2
elif alien_0['speed']=='fast':
    x_increment=3
alien_0['x_position']=alien_0['x_position']+x_increment
print(f"New position{alien_0['x_position'],alien_0['y_position']}")
print(alien_0)
del alien_0['points']
print(alien_0)
favourite_languages = {
    'jen':'python',
    'sarah':'c',
    'edward':'ruby',
    'phil':'go'
}
language=favourite_languages['sarah'].title()
print(f"Sarah's favourite language is {language}.")
point_value=alien_0.get('points','No point value assighed.')
print (point_value)
# for k,v in favourite_languages.items():
#     print(f"\n{k}'s favourite language is{v}")
#     # print(f"Favourite language:{v}")
# for name in favourite_languages.keys():
#     print(name.title())
# # 创建第一个外星人字典，包含颜色和点数属性
# alien_1={'color':'red','points':5} """这是一个创建外星人字典并将它们存储在列表中的简单示例展示了如何创建多个字典并将它们组合成列表"""# 创建第一个外星人字典，包含颜色和点数属性
# # 创建第二个外星人字典，包含颜色和点数属性
# alien_2={'color':'blue','points':6}
# # 创建第三个外星人字典，包含颜色和点数属性
# alien_3={'color':'pink','points':7}
# # 将三个外星人字典放入一个列表中
# aliens=[alien_1,alien_2,alien_3]
# # 打印外星人列表 ，输出结果为[{'color': 'red', 'points': 5}, {'color': 'blue', 'points': 6}, {'color': 'pink', 'points': 7}]
# print(aliens)

# aliens=[]
# for alien_number in range(30):
#     new_alien={'color':'green','points':5,'speed':'slow'}
#     aliens.append(new_alien)
# for alien in aliens[:3]:
#     if alien['color']=='green':
#         alien['color']='yellow'
#         alien['speed']='medium'
#         alien['points']=10
#     elif alien['color']=='yellow':
#         alien['color']='red'
#         alien['points']=50
#         alien['speed']='Very Fast'
# for alien in aliens[:5]: #  遍历前5个外星人
#     print(alien) #  打印每个外星人的信息
# print (f"Total number of aliens:{len(aliens)}") #  打印外星人的总数
# print('---------------------------------------------------------------------------\n') #  打印分隔线
# for alien in aliens[:3]: #  遍历前3个外星人
#     if alien['color']=='green': #  如果外星人的颜色是绿色
#         alien['color']='yellow' #  将颜色改为黄色
#         alien['speed']='medium' #  速度设置为中等
#         alien['points']=10 #  分数设置为10
#     elif alien['color']=='yellow': #  如果外星人的颜色是黄色
#         alien['color']='red' #  将颜色改为红色
#         alien['points']=50 #  分数设置为50
#         alien['speed']='Very Fast' #  速度设置为非常快
# for alien in aliens[:5]: #  再次遍历前5个外星人
#     print(alien) #  打印每个外星人的信息
# print (f"Total number of aliens:{len(aliens)}") #  打印外星人的总数



# Pizza={
#     'crust':'thick',
#     'toppings':['mushrooms','extra cheese'],
# }
# print (f"You ordered a {Pizza['crust']}-crust pizza" "with the following toppings")
# for topping in Pizza['toppings']:
#     print(topping)

# favourite_languages={ #  定义一个字典，存储不同人的喜欢的编程语言
#     'jen':['python','c'], #  jen喜欢的编程语言列表
#     'sarah':['c'], #  sarah喜欢的编程语言列表
#     'edward':['ruby','go'], #  edward喜欢的编程语言列表
#     'phil':['python','haskell'], #  phil喜欢的编程语言列表
    
# }
# for name,languages in favourite_languages.items(): #  遍历字典中的每个键值对
#     print(f"\n{name.title()}'s favourite languages are:") #  打印每个人的名字和他们喜欢的编程语言
#     for language in languages: 
#         print(f"\t{language.title()}")  # 打印每个语言的标题版本 
        
# users={ #  创建一个字典users，存储用户信息
#     'aeinstein':{ #  用户aeinstein的信息
#         'first':'albert', #  名
#         'last':'einstein', #  姓
#         'location':'princeton', #  位置
#     },
#     'mcurie':{ #  用户mcurie的信息
#         'first':'marie', #  名
#         'last':'curie', #  姓
#         'location':'paris', #  位置
#     },
# }
# for username,user_info in users.items(): #  遍历users字典中的每个用户
#     print(f"\nUsername:{username}") #  打印用户名
#     full_name=f"{user_info['first']} {user_info['last']}" #  将用户的名和姓组合成全名
#     location=user_info['location'] #  获取用户的位置信息
#     print(f"\tFull name:{full_name.title()}") #  打印格式化后的全名（首字母大写）
#     print(f"\t\tLocation:{location.title()}") #  打印格式化的位置信息，使用制表符进行缩进，并将位置字符串首字母大写
# message=input("Tell me something,and I will repeat it back to you: ")
# print (message)
# name = input("Please enter your name: ")
# print (f"Hello {name},nice to meet you!")
# prompt = "If you tell us who you are, we can personalize the messages you see."
# prompt+="\n\t\tWhat is your first name? "
# name=input(prompt)
# print(f"Hello,{name}!")

# age = input("How old are you? ")
# age=int(age)
# print(5%3)

# number=input("Enter a number,and I will tell you if it's even or odd:\n ")
# number=int(number)
# if number%2==0:
#     print(f" {number} is even")
# else:
#     print(f" {number} is odd")

# current_number=1
# while current_number<=5:
#     print(current_number)
#     current_number += 1

# prompt="\nTell me something, and I will repeat it back to you " #  定义一个提示字符串变量
# prompt+="\nEnter 'quit' to exit the game." 
# message=""
# while message!='quit':
#     message = input(prompt)
#     if message!='quit':
#         print (message)
    
# prompt="\nTell me something, and I will repeat it back to you " #  定义一个提示字符串变量
# prompt+="\nEnter 'quit' to exit the game." 
# # message=""
# flag=True
# while (flag):
#     message=input(prompt)
#     if message=='quit':
#         flag=False
#     else:
#         print(message)

# while True:
#     message_a=input('\ngive me some words  \t\n')
#     if message_a=='quit':
#         break
#     else:
#         print(message_a)

# current_number_A=0 #  初始化变量current_number_A为0
# while current_number_A<10: #  当current_number_A小于10时，执行循环
#     current_number_A+=1 #  每次循环将current_number_A加1
#     if  current_number_A%2==0: #  如果current_number_A是偶数，则跳过本次循环的剩余部分
#         continue
#     print(current_number_A) #  打印奇数current_number_A的值

# x=1
# while x <=5:
#     print(x)
#     x+=1

# unconfirmed_users=['alice','brian','candace'] #  初始化一个未验证用户列表
# confirmed_users=[] #  初始化一个空列表用于存储已验证的用户
# while unconfirmed_users: #  当未验证用户列表不为空时，继续循环
#     current_user=unconfirmed_users.pop() #  从未验证用户列表中弹出最后一个用户
#     print(f"Verifying user:{current_user.title()}") #  打印正在验证的用户信息
#     confirmed_users.append(current_user) #  将已验证的用户添加到已验证用户列表中
# print ("\nThe following users have been confirmed: ") #  打印提示信息，表示即将显示已验证的用户列表
# for confirmed_user in confirmed_users: #  遍历已验证用户列表
#     print(confirmed_user.title()) #  打印每个已验证用户的名称（首字母大写）

# pets = ['dog','cat','dog','goldfish','cat','rabbit','cat'] #  定义一个包含多种宠物的列表
# print(pets) #  打印初始的宠物列表
# while 'cat' in pets: #  当列表中还存在'cat'元素时，循环执行删除操作
#     pets.remove('cat') #  移除列表中第一个出现的'cat'
#     print (pets) #  打印每次删除'cat'后的列表状态

# responses={} #  创建一个空字典，用于存储用户调查结果
# polling_active= True #  设置一个标志，控制调查是否继续进行
# while polling_active: #  当调查处于活动状态时，执行循环
#     name=input("What is your name? ") #  获取用户姓名
#     response=input("Which mountain would you like to climb someday?") #  获取用户想要攀登的山峰
#     responses[name]=response # !(关键就是这一条，是新增或者修改键值对的方法) 将被调查者的姓名和回应存储到字典中
#     repeat =input ("Would you like to let another person respond(yes/no)") #  询问用户是否想让另一个人参与调查
#     if repeat =='no': #  如果用户输入"yes"，则结束调查并显示结果
#         polling_active=False
#         print ("\n---Poll Results ---")
#         for name,response in responses.items(): #  遍历字典中的所有条目，打印调查结果
#             print (f"{name} would like to climb {response}")


# def greet_users(username):

#     """
#     该函数用于向用户发送欢迎信息
#     参数:
#         username: 用户名，用于个性化欢迎信息
#     """
#     print (f"Hello,{username.title()}")  # 打印个性化的问候语，首字母大写
#     print("Welcome to ShineUni Tech")
#     print ("Have a good day")
# while True:   # 无限循环，持续运行直到遇到break语句
#     username=input("Please enter your name\n\t")  # 提示用户输入用户名，\t用于缩进显示
#     if(username=='quit'):  # 检查用户输入是否为'quit'，如果是则退出循环
#         break
#     greet_users(username)  # 调用greet_users函数，传入用户名作为参数
    
    
# def jiecheng(x):
#     # 初始化计数器i为1
#     i=1
#     # 初始化结果变量result为1
#     result=1
#     # 使用while循环计算x的阶乘
#     while i <=x:
#         # 将result乘以当前的i值
#         result*=i
#         # 计数器i递增1
#         i+=1
#     # 打印计算结果
#     print(result)

# def describe_pet(pet_name,animal_type='dog'):
#     '''显示宠物的信息'''
#     print(f"\nI have a {animal_type}")
#     print(f"My {animal_type}'s name is {pet_name.title()}.")

# describe_pet(animal_type='Corgi',pet_name='Fuzai')
# describe_pet('zaizai')

# def get_formatted_name(first_name,last_name,middle_name=''):
#     if middle_name:
#         full_name=f"{first_name} {middle_name} {last_name}" #  拼接全名 如果有中间名，则格式为：名 中间名 姓 如果没有中间名，则格式为：名 姓
#     else:
#         full_name=f"{first_name} {last_name}" #  拼接不包含中间名的全名
#     return full_name.title() #  返回格式化后的全名，首字母大写
# musician=get_formatted_name('john','booker') #  调用get_formatted_name函数，传入参数'john'和'booker'
# print (musician) #  打印格式化后的名字

# def build_person(first_name,last_name):
#     person={'first':first_name,'last':last_name}
#     return person #  返回包含人员信息的字典
# musician=build_person('jimi','hendrix') #  调用build_person函数，传入名字'jimi'和姓氏'hendrix'，并将返回结果存储在musician变量中
# print(musician['first']) #  打印人员字典中的名字(first)信息
# print(musician['last']) #  打印人员字典中的姓氏(last)信息

# def build_person(first_name,last_name,age=None):
#     person={'first':first_name,'last':last_name}
#     if age: #  如果age参数不为空，则将age添加到person字典中
#         person['age']=age
#     return person #  返回包含人物信息的字典
# musician=build_person('jimi','hendrix',age=23) #  创建一个音乐家人物信息字典，名字为jimi，姓氏为hendrix，年龄为23
# print(musician) #  打印整个musician字典
# print(musician['first']) #  打印音乐家的名字
# print(musician['last']) #  打印音乐家的姓氏
# print(musician['age']) #  打印音乐家的年龄

# def get_formatted_name(first_name,last_name):
#     full_name=f"{first_name} {last_name}"
#     return full_name.title()
# while True:
#     print("\nPlease tell me your name:")
#     print("(enter 'q' at any time to quit)") #  提示用户随时输入'q'退出
#     f_name=input("First name: ") #  获取用户输入的名字
#     if f_name=='q': #  检查用户是否想退出
#         break
#     l_name=input("Last name: ") #  获取用户输入的姓氏
#     if l_name=='q': #  再次检查用户是否想退出
#         break
#     formatted_name=get_formatted_name(f_name,l_name) #  调用函数格式化姓名
#     print(f"Hello,{formatted_name}!") #  打印格式化后的问候语


# 酒店管理系统（控制台版本）
# def init_hotel_rooms():
#     """初始化酒店房间，返回房间字典"""
#     # 房间结构：{房间号: {状态, 客人姓名, 入住天数, 每日房价}}
#     rooms = {}
#     for room_num in range(101, 106):  # 初始化101-105共5间房
#         rooms[room_num] = {
#             "status": "空闲",  # 房间状态：空闲/已入住
#             "guest_name": "",  # 客人姓名
#             "check_in_days": 0,  # 入住天数
#             "daily_price": 299  # 每日房价（默认299元/天）
#         }
#     return rooms

# def show_menu():
#     """显示系统菜单"""
#     print("=" * 30)
#     print("    欢迎使用XX酒店管理系统")
#     print("=" * 30)
#     print("1. 查看所有房间状态")
#     print("2. 房间入住登记")
#     print("3. 房间退房结算")
#     print("4. 退出系统")
#     print("=" * 30)

# def show_all_rooms(rooms):
#     """查看所有房间的当前状态"""
#     print("\n当前酒店房间状态如下：")
#     print("房间号\t状态\t\t客人姓名\t\t应付总价（元）")
#     print("-" * 60)
#     for room_num, room_info in rooms.items():
#         # 计算总价：入住天数 * 每日房价
#         total_price = room_info["check_in_days"] * room_info["daily_price"]
#         # 格式化输出，让界面更整齐
#         print(f"{room_num}\t{room_info['status']}\t\t{room_info['guest_name'] or '无'}\t\t{total_price if room_info['status'] == '已入住' else 0}")
#     print("\n")

# def check_in_room(rooms):
#     """办理房间入住手续"""
#     try:
#         room_num = int(input("请输入要入住的房间号（101-105）："))
#         # 检查房间号是否存在
#         if room_num not in rooms:
#             print("错误：该房间不存在！")
#             return
#         # 检查房间是否已空闲
#         room_info = rooms[room_num]
#         if room_info["status"] == "已入住":
#             print(f"错误：{room_num}房间已被入住，无法重复登记！")
#             return
#         # 收集入住信息
#         guest_name = input("请输入客人姓名：").strip()
#         if not guest_name:
#             print("错误：客人姓名不能为空！")
#             return
#         check_in_days = int(input("请输入入住天数："))
#         if check_in_days <= 0:
#             print("错误：入住天数必须大于0！")
#             return
#         # 更新房间信息（标记为已入住）
#         room_info["status"] = "已入住"
#         room_info["guest_name"] = guest_name        
#         room_info["check_in_days"] = check_in_days
#         print(f"恭喜！{guest_name}已成功入住{room_num}房间，入住{check_in_days}天，每日房价{room_info['daily_price']}元。")
#     except ValueError:
#         print("错误：输入格式不正确，请输入数字！")

# def check_out_room(rooms):
#     """办理房间退房结算"""
#     try:
#         room_num = int(input("请输入要退房的房间号（101-105）："))
#         # 检查房间号是否存在
#         if room_num not in rooms:
#             print("错误：该房间不存在！")
#             return
#         # 检查房间是否已入住
#         room_info = rooms[room_num]
#         if room_info["status"] == "空闲":
#             print(f"错误：{room_num}房间当前为空闲状态，无需退房！")
#             return
#         # 计算结算金额
#         total_price = room_info["check_in_days"] * room_info["daily_price"]
#         print(f"\n退房结算单：")
#         print(f"房间号：{room_num}")
#         print(f"客人姓名：{room_info['guest_name']}")
#         print(f"入住天数：{room_info['check_in_days']}天")
#         print(f"每日房价：{room_info['daily_price']}元")
#         print(f"应结算总金额：{total_price}元")
#         # 确认退房（重置房间状态）
#         confirm = input("\n是否确认退房？（y/n）：").lower()
#         if confirm == "y":
#             room_info["status"] = "空闲"
#             room_info["guest_name"] = ""
#             room_info["check_in_days"] = 0
#             print(f"{room_num}房间退房成功！欢迎客人下次光临～")
#         else:
#             print("退房操作已取消！")
#     except ValueError:
#         print("错误：输入格式不正确，请输入数字！")

# def main():
#     """系统主函数，控制整体流程"""
#     # 初始化房间
#     hotel_rooms = init_hotel_rooms()
#     while True:
#         # 显示菜单
#         show_menu()
#         try:
#             choice = int(input("请输入您的操作选择（1-4）："))
#             # 根据选择执行对应功能
#             if choice == 1:
#                 show_all_rooms(hotel_rooms)
#             elif choice == 2:                   
#                 check_in_room(hotel_rooms)  
#             elif choice == 3:
#                 check_out_room(hotel_rooms)
#             elif choice == 4:
#                 print("感谢使用XX酒店管理系统，祝您生活愉快，再见！")
#                 break
#             else:
#                 print("错误：请输入1-4之间的有效数字！")
#         except ValueError:
#             print("错误：输入格式不正确，请输入数字！")
#         # 每次操作后换行，优化界面体验

#         input("\n按回车键继续...")

# # 运行系统
# if __name__ == "__main__":
#     main()

def build_person(first_name,last_name):
    person={'first':first_name,'last':last_name}
    return person #  返回包含个人信息的字典
musician=build_person('Zhenyu','Yu') #  创建一个音乐家对象，调用build_person函数，传入名字'Zhenyu'和姓氏'Yu'
name = musician['last'] #  获取音乐家的姓氏
name += musician['first'] #  将姓氏和名字拼接在一起
print(name) #  打印拼接后的完整姓名

