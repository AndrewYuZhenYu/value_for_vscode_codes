package main

//hello.go
import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Println("=== Go 语言基础输入与输出演示 ===")

	// --------------------------------------------------
	// 方式一：fmt.Scanln / fmt.Scan（适合输入单个单词、数字等）
	// --------------------------------------------------
	var name string
	var age int

	fmt.Print("1. 请输入你的姓名和年龄 (用空格隔开，如: Tom 20): ")
	// 类似 C 语言的 scanf("%s %d", &name, &age)
	fmt.Scanln(&name, &age)

	// 格式化输出 (Println 换行打印，Printf 格式化打印)
	fmt.Printf("-> 收到: 姓名 = %s, 年龄 = %d 岁\n\n", name, age)

	// --------------------------------------------------
	// 方式二：bufio.Scanner（适合读取包含空格的一整行文本）
	// --------------------------------------------------
	reader := bufio.NewScanner(os.Stdin)

	fmt.Print("2. 请输入一句包含空格的长句子 (例如个人座右铭): ")
	if reader.Scan() {
		sentence := reader.Text()

		// 演示简单的字符串处理输出
		upperSentence := strings.ToUpper(sentence)
		fmt.Printf("-> 原文: %s\n", sentence)
		fmt.Printf("-> 大写: %s\n", upperSentence)
		fmt.Printf("-> 字符长度: %d\n\n", len(sentence))
	}

	// --------------------------------------------------
	// 常见格式化输出占位符演示 (Printf)
	// --------------------------------------------------
	score := 98.5678
	isPassed := true

	fmt.Println("=== 常用格式化占位符演示 ===")
	fmt.Printf("布尔值 (%%t): %t\n", isPassed)
	fmt.Printf("浮点数保留两位 (%%.2f): %.2f\n", score)
	fmt.Printf("打印变量类型 (%%T): %T\n", score)
	fmt.Printf("通用值打印 (%%v): %v\n", score)
}
