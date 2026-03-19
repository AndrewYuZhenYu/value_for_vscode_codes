#include<stdio.h>
#include<string.h>
int main()
{
    char s[1000];
    fgets(s,sizeof(s),stdin);
    s[strcspn(s,"\n")]='\0';
    int count=0;
    for (int i=0;s[i]!='\0';i++)
    {
        if(s[i]==' '&&s[i+1]!=' '&&s[i+1]!='\0')
        {
            count++;
        }
        
        
        
    }
    
    if(s[0]!=' ')count++;
    
    printf("%d",count);
}
 