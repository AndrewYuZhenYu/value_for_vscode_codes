/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // 为返回的结果分配空间，题目要求返回 2 个下标
    int* result = (int*)malloc(sizeof(int) * 2);
    
    for (int i = 0; i < numsSize; i++) {
        for (int j = i + 1; j < numsSize; j++) {
            if (nums[i] + nums[j] == target) {
                result[0] = i;
                result[1] = j;
                *returnSize = 2; // 必须告诉调用者数组长度是 2
                return result;
            }
        }
    }
    
    *returnSize = 0;
    return NULL;
}