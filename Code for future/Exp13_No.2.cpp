#include <stdio.h>
#include <string.h>

// (1) 检查两个字符串是否由同样的字符组成
int hasSameChars(const char *s1, const char *s2) {
    int count[256] = {0};
    
    // 统计s1的字符
    for (; *s1; s1++) {
        count[(unsigned char)*s1]++;
    }
    
    // 统计s2的字符并抵消
    for (; *s2; s2++) {
        count[(unsigned char)*s2]--;
    }
    
    // 检查是否有剩余
    for (int i = 0; i < 256; i++) {
        if (count[i] != 0) {
            return 0;
        }
    }
    return 1;
}

// (2) 判断一个字符串是否可以通过另一个字符串重排得到
int canBeRearranged(const char *s1, const char *s2) {
    return hasSameChars(s1, s2);
}

int main() {
    char str1[100], str2[100];
    
    printf("请输入第一个字符串: ");
    fgets(str1, sizeof(str1), stdin);
    str1[strcspn(str1, "\n")] = '\0';
    
    printf("请输入第二个字符串: ");
    fgets(str2, sizeof(str2), stdin);
    str2[strcspn(str2, "\n")] = '\0';
    
    // 测试函数
    printf("两个字符串由同样的字符组成吗？ %s\n", 
           hasSameChars(str1, str2) ? "是" : "否");
    printf("一个字符串可以通过另一个重排得到吗？ %s\n",
           canBeRearranged(str1, str2) ? "是" : "否");
    
    return 0;
}