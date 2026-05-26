import requests
import pandas as pd
import time

# ==================== 配置区域 ====================
# 1. 把你在浏览器 F12 复制的真实 Cookie 粘贴到下方单引号内
COOKIE = 'fid=24676; 24676enc=F29A778B27C7656C160D03A6C05C568D; 24676userinfo=803cc972880aed75874ed889cc4fef0888b83130e7eb4704a7346ef98d28f331c98bf515e9147871f9ec4f2c6b581551e7fafd565af53bf2; lv=0; vc=F29A778B27C7656C160D03A6C05C568D; xxtenc=d0f1ce512b145e38870d6d1b5fdafd25; UID=670; 24676UID=670; _uid=670; vc2=8EC09CCD446DD498EAD456191B8FA54A; _d=1778400358750; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2NzAiLCJsb2dpblRpbWUiOjE3Nzg0MDAzNTg3NTAsImV4cCI6MTc3OTAwNTE1OH0.sEajydYifz0KtSG9L24bhWGt3Z4m-s23_un_xkUb7OY; vc3=iOuiSbrHC1p0YY1Ek95Rkd2imQ0yYYaRkKV21Wrbm4lohI6dHqnF%2Boosq1JxKEWNnlGBsK60l7DrE9mR0czfZJ2J840GhsH2CIuJBOZEJd8DgnC1B7yEE4J8sk3PI7LKpkIDQkoGj8ZKi9QEOVv4AlCo6kKfqVJTSIzN%2FYMF2Mc%3D1a92cd7f0f755175369d6bcc86af31be; uf=da0883eb5260151e86421c4a8b60a0064764bfa6814c95bb25ccf7e7163806a510ffe85ee3ed17e95af3b400428320075cf121817f5c2c62a94b593de5d847e4d8a8d0ca21d204ebbfecd4077347b641d1d3a69a85a4c7dd6d2b2f5c733458be; DSSTASH_LOG=C_38-UN_0-US_670-T_1778400358750; csrftoken=ZAOPgI6f4j5JObcrpFUbLAoTrSgzI8Q4; sessionid=7i94dgkcxskg8ers9tj1zmsnjfesr0ap'

# 2. 预估的总页数（根据你说的二十多页，这里默认设为 25，脚本遇到空页会自动提前停止）
TOTAL_PAGES = 25
# ==================================================

# 伪装浏览器请求头
headers = {
    'Cookie': COOKIE,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

all_dataframes = []

print("🚀 爬虫启动，开始抓取专业分流数据...")

for page in range(1, TOTAL_PAGES + 1):
    print(f"正在抓取第 {page}/{TOTAL_PAGES} 页...")
    url = f"https://aa.bjtu.edu.cn/transfer_major/transmajorresult/notice/?page={page}"
    
    try:
        # 发起网络请求
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # 强制使用 utf-8 编码防止中文乱码
        
        # 检查是否成功返回网页
        if response.status_code != 200:
            print(f"❌ 第 {page} 页请求失败，状态码: {response.status_code}，可能是 Cookie 过期了。")
            break
            
        # 使用 pandas 直接解析 HTML 中的 <table> 标签
        tables = pd.read_html(response.text)
        
        if tables:
            df = tables[0]
            
            # 验证表格里是否真的有数据（通过判断有没有“学号”这一列）
            if not df.empty and '学号' in df.columns:
                all_dataframes.append(df)
                print(f"✅ 第 {page} 页抓取成功，获取到 {len(df)} 条记录。")
            else:
                print(f"💡 第 {page} 页表格内容为空或结构不符，判断已无更多数据，停止抓取。")
                break
        else:
            print(f"💡 第 {page} 页未找到表格，停止抓取。")
            break
            
    except Exception as e:
        print(f"💥 抓取第 {page} 页时发生异常: {e}")
        break
        
    # 礼貌爬取：每页抓完休眠 2 秒，避免给学校服务器带来太大压力
    time.sleep(2)

# ==================== 数据合并与保存 ====================
if all_dataframes:
    print("\n📊 正在合并所有页面数据...")
    # 将所有 DataFrame 拼接成一个大表
    final_df = pd.concat(all_dataframes, ignore_index=True)
    
    # 清洗数据：过滤掉可能因为分页重复生成的表头行
    # 确保“学号”列里都是纯数字，如果混入了文字“学号”则过滤掉
    final_df = final_df[final_df['学号'].astype(str).str.isdigit()]
    
    # 导出到 Excel
    file_name = "北京交通大学专业分流录取结果.xlsx"
    final_df.to_excel(file_name, index=False)
    print(f"🎉 【大功告成】所有人名单已完美整合！文件已保存至当前目录下的：{file_name}")
else:
    print("\n❌ 未能抓取到任何有效数据，请检查配置区域的 Cookie 是否正确复制。")