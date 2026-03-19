/*大气方能成大器，有德不必求有得*/
#include<stdio.h>
#include<string.h>
int main()
{
int N;
scanf("%d",&N);
getchar();

char names[N][51];
int nums[N];
for (int i=0;i<N;i++)
{
    fgets(names[i],sizeof(names[i]),stdin);
   names[i][strcspn(names[i],"\n")]='\0';
   nums[i]=i+1;
}
char c[50];
fgets(c,sizeof(c),stdin);
c[strcspn(c,"\n")]='\0';
int count=0;
for (int i=0;i<N;i++)
{
    if(strcmp(c,names[i])==0)
    {
        printf("%d",nums[i]);
        count++; 
        break;       
    }
    
}
if(count==0)printf("-1");
}
