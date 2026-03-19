#include<stdio.h>
int main()
{
    int M,N;
    scanf("%d%d",&N,&M);
    int mar[N][M];
    for (int i=0;i<N;i++)
    {
        for (int j=0;j<M;j++)
        {
            scanf("%d",&mar[i][j]);
        }
    }
    int count=0;
    int row[N*M];
    int column[N*M];
    int elements[N*M];
    for (int i=0;i<N;i++)
    {
        for (int j=0;j<M;j++)
        {
            if(mar[i][j]!=0)
            {
                row[count]=i;
                column[count]=j;
                elements[count]=mar[i][j];
                count++;
            }
        }
    }
    printf("%d %d %d\n",N,M,count);
    for(int i=0;i<count;i++)
    {
        printf("%d %d %d\n",row[i],column[i],elements[i]);
    }

}