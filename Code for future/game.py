import random

def guess_number():
    # 生成 1 到 100 之间的随机整数
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print("-" * 30)
    print("欢迎来到猜数字挑战赛！")
    print("我已经想好了一个 1 到 100 之间的数字。")
    print("-" * 30)

    while True:
        try:
            # 获取用户输入
            guess = int(input("请输入你猜的数字: "))
            attempts += 1

            # 比较逻辑
            if guess < secret_number:
                print("太小了！再试大一点。")
            elif guess > secret_number:
                print("太大了！再试小一点。")
            else:
                print(f"🎉 恭喜你！你猜对了！")
                print(f"这个数字就是 {secret_number}。")
                print(f"你一共尝试了 {attempts} 次。")
                break # 猜对了，跳出循环
        except ValueError:
            # 捕获输入非数字时的错误
            print("输入无效！请输入一个有效的整数。")

if __name__ == "__main__":
    guess_number()