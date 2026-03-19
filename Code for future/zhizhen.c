#include<stdio.h>
#define STUD_NUM 5

struct Stud{
	int No;
	int Score[2];
};

void main()
{
      struct Stud StudAll[STUD_NUM], StudTmp;
      int ScoreSum[STUD_NUM] = {0};
      int i;

      for(i = 0; i < STUD_NUM; i++)
            scanf_s("%d%d%d", &StudAll[i].No, &StudAll[i].Score[0], &StudAll[i].Score[1]);

      for(i = 0; i < STUD_NUM; i++)
            if (StudAll[i].Score[0] < 60 || StudAll[i].Score[1] < 60)
                  printf("%d\n", StudAll[i].No);
}
