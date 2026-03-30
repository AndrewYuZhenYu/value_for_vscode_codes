# 使用方法修改字符串的大小写
test_1="I Love The University of Hong Kong"
print (test_1.title())
print (test_1.upper())
print (test_1.lower())
#合并(拼接)字符串
first_name = "ada" 
last_name = "lovelace" 
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
