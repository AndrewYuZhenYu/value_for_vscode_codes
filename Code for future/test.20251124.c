#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_DAYS 31
#define WIDTH 60
#define HEIGHT 20

typedef struct
{
    char date[11]; // YYYY-MM-DD
    float open;    // 开盘价
    float high;    // 最高价
    float low;     // 最低价
    float close;   // 收盘价
    float change;  // 涨跌幅
} StockData;

// 模拟生成上证指数数据（实际应用中应该从API获取真实数据）
void generateMockData(StockData data[], int days)
{
    srand(time(NULL));
    float basePrice = 3200.0f; // 基准价格

    for (int i = 0; i < days; i++)
    {
        // 生成日期
        sprintf(data[i].date, "2025-12-%02d", 15 + i);

        // 生成随机但相对合理的股价变动
        float changeRate = ((float)(rand() % 201 - 100)) / 1000.0f; // -10% to +10%
        float currentPrice = basePrice * (1 + changeRate);

        data[i].open = currentPrice + ((float)(rand() % 21 - 10)) / 100.0f;
        data[i].high = data[i].open + ((float)(rand() % 51)) / 100.0f;
        data[i].low = data[i].open - ((float)(rand() % 51)) / 100.0f;
        data[i].close = data[i].open + ((float)(rand() % 41 - 20)) / 100.0f;

        // 确保高低价合理
        if (data[i].low > data[i].open)
            data[i].low = data[i].open - 0.1f;
        if (data[i].high < data[i].open)
            data[i].high = data[i].open + 0.1f;

        data[i].change = (data[i].close - data[i].open) / data[i].open * 100;
        basePrice = data[i].close;
    }
}

// 清屏函数
void clearScreen()
{
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

// 绘制K线图
void drawKLineChart(StockData data[], int days)
{
    printf("\n=== 上证指数近%d天K线走势图 ===\n\n", days);

    // 找到最高价和最低价用于缩放
    float maxPrice = data[0].high, minPrice = data[0].low;
    for (int i = 1; i < days; i++)
    {
        if (data[i].high > maxPrice)
            maxPrice = data[i].high;
        if (data[i].low < minPrice)
            minPrice = data[i].low;
    }

    float priceRange = maxPrice - minPrice;
    float scaleY = HEIGHT / priceRange;

    // 绘制坐标轴
    printf("价格(点)\n");
    for (int i = HEIGHT; i >= 0; i--)
    {
        float priceLevel = minPrice + (priceRange * i / HEIGHT);
        printf("%8.1f |", priceLevel);

        // 绘制网格线和价格标签
        if (i % 5 == 0)
        {
            for (int j = 0; j < WIDTH; j++)
                printf("-");
        }
        else
        {
            for (int j = 0; j < WIDTH; j++)
                printf(" ");
        }
        printf("\n");
    }

    // 绘制K线
    printf("          ");
    for (int j = 0; j < WIDTH; j++)
        printf("--");
    printf(" 日期\n");

    for (int day = 0; day < days && day < WIDTH; day++)
    {
        StockData today = data[day];

        // 计算坐标位置
        int x = day * WIDTH / days;
        int yHigh = (int)((today.high - minPrice) * scaleY);
        int yLow = (int)((today.low - minPrice) * scaleY);
        int yOpen = (int)((today.open - minPrice) * scaleY);
        int yClose = (int)((today.close - minPrice) * scaleY);

        // 绘制垂直线（最高价到最低价）
        for (int y = 0; y <= HEIGHT; y++)
        {
            // 这里需要更复杂的逻辑来绘制精确的K线
        }

        // 简化的K线表示：红色上涨，绿色下跌
        char candleChar = (today.close >= today.open) ? '+' : '-';
        printf("%s [%c]", today.date + 5, candleChar); // 只显示月-日

        // 在底部显示涨跌幅
        if (today.change > 0)
        {
            printf("\033[31m+%.2f%%\033[0m ", today.change); // 红色
        }
        else
        {
            printf("\033[32m%.2f%% \033[0m ", today.change); // 绿色
        }
    }
    printf("\n");
}

// 绘制折线图
void drawLineChart(StockData data[], int days)
{
    printf("\n=== 上证指数收盘价走势图 ===\n\n");

    float maxPrice = data[0].close, minPrice = data[0].close;
    for (int i = 1; i < days; i++)
    {
        if (data[i].close > maxPrice)
            maxPrice = data[i].close;
        if (data[i].close < minPrice)
            minPrice = data[i].close;
    }

    float priceRange = maxPrice - minPrice;
    float scaleY = HEIGHT / priceRange;

    // 绘制图表区域
    char chart[HEIGHT + 1][WIDTH + 1];
    memset(chart, ' ', sizeof(chart));

    // 填充数据点
    for (int day = 0; day < days && day < WIDTH; day++)
    {
        int x = day * WIDTH / days;
        int y = HEIGHT - (int)((data[day].close - minPrice) * scaleY);

        if (y >= 0 && y <= HEIGHT)
        {
            chart[y][x] = '*';
        }

        // 连接线
        if (day > 0)
        {
            int prevX = (day - 1) * WIDTH / days;
            int prevY = HEIGHT - (int)((data[day - 1].close - minPrice) * scaleY);

            // 简单的连线算法
            int dx = x - prevX;
            int dy = y - prevY;
            int steps = (abs(dx) > abs(dy)) ? abs(dx) : abs(dy);

            for (int step = 1; step <= steps; step++)
            {
                int cx = prevX + (dx * step / steps);
                int cy = prevY + (dy * step / steps);

                if (cx >= 0 && cx < WIDTH && cy >= 0 && cy <= HEIGHT)
                {
                    chart[cy][cx] = '.';
                }
            }
        }
    }

    // 打印图表
    printf("价格范围: %.2f - %.2f\n\n", minPrice, maxPrice);

    for (int i = 0; i <= HEIGHT; i++)
    {
        float priceLevel = minPrice + (priceRange * (HEIGHT - i) / HEIGHT);
        printf("%8.1f |", priceLevel);

        for (int j = 0; j < WIDTH; j++)
        {
            putchar(chart[i][j]);
        }
        printf("\n");
    }

    // 打印底部标签
    printf("          ");
    for (int day = 0; day < days && day < WIDTH; day++)
    {
        printf("%c", data[day].date[strlen(data[day].date) - 3]); // 显示日的个位数
    }
    printf("\n");
}

// 显示数据统计信息
void displayStatistics(StockData data[], int days)
{
    printf("\n=== 统计信息 ===\n");

    float sum = 0, maxChange = data[0].change, minChange = data[0].change;
    float highest = data[0].high, lowest = data[0].low;

    for (int i = 0; i < days; i++)
    {
        sum += data[i].change;
        if (data[i].change > maxChange)
            maxChange = data[i].change;
        if (data[i].change < minChange)
            minChange = data[i].change;
        if (data[i].high > highest)
            highest = data[i].high;
        if (data[i].low < lowest)
            lowest = data[i].low;
    }

    printf("平均涨跌幅: %.2f%%\n", sum / days);
    printf("最大涨幅:   %.2f%%\n", maxChange);
    printf("最大跌幅:   %.2f%%\n", minChange);
    printf("期间最高:   %.2f点\n", highest);
    printf("期间最低:   %.2f点\n", lowest);
    printf("波动幅度:   %.2f点\n", highest - lowest);
}

int main()
{
    StockData stockData[MAX_DAYS];
    int days = 30; // 显示最近30天数据

    // 生成模拟数据
    generateMockData(stockData, days);

    int choice;
    do
    {
        clearScreen();
        printf("=== 上证指数分析系统 ===\n");
        printf("1. K线图显示\n");
        printf("2. 折线图显示\n");
        printf("3. 统计信息\n");
        printf("4. 显示所有数据\n");
        printf("0. 退出\n");
        printf("请选择功能: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            clearScreen();
            drawKLineChart(stockData, days);
            break;
        case 2:
            clearScreen();
            drawLineChart(stockData, days);
            break;
        case 3:
            clearScreen();
            displayStatistics(stockData, days);
            break;
        case 4:
            clearScreen();
            printf("日期\t\t开盘\t最高\t最低\t收盘\t涨跌\n");
            printf("--------------------------------------------------\n");
            for (int i = 0; i < days; i++)
            {
                printf("%s\t%.2f\t%.2f\t%.2f\t%.2f\t",
                       stockData[i].date, stockData[i].open,
                       stockData[i].high, stockData[i].low,
                       stockData[i].close);

                if (stockData[i].change > 0)
                {
                    printf("\033[31m+%.2f%%\033[0m\n", stockData[i].change);
                }
                else
                {
                    printf("\033[32m%.2f%%\033[0m\n", stockData[i].change);
                }
            }
            break;
        case 0:
            printf("感谢使用！\n");
            break;
        default:
            printf("无效选择！\n");
        }

        if (choice != 0)
        {
            printf("\n按回车键继续...");
            getchar(); // 清除输入缓冲区
            getchar(); // 等待回车
        }

    } while (choice != 0);

    return 0;
}