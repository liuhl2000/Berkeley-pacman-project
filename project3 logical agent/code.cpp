#include<stdio.h>
#include<iostream>
#include<string.h>
using namespace std;

const long int mod = 2181271;
const long int p = 233;
// use p and mod to generate 1 to x^25

int weight[26] =  {3881, 1974535, 365312, 2130993, 1185472, 516293, 1326355,\
    1965466, 68859, 1126717, 1521593, 601836, 1765546, 711815, 1064929, 1662175,\
    882828, 1659998, 1158975, 201173, 2038666, 592829, 1709715, 2158804, 56413, 811753};
/*long long int hash_function(int* array, int len){
    long long hash_value = 0;
	for(int i = 0; i < len; ++i){
		hash_value = (hash_value*p + array[i]) % mod;
	}
	return hash_value;
}*/

long long int hash_function(int* array, int len){
    long long hash_value = 0;
	for(int i = 0; i < len; ++i){
		hash_value = hash_value + array[i]*weight[i];
    }
  	hash_value = hash_value&((1<<21) - 1);
	return hash_value;
}

typedef struct node{
    int* value;
    struct node* next;
} node;

class linked_list
{
public:
    linked_list();
    ~linked_list();
    void append(int* value);
    bool check_equal(int* value);
    int getlen();
    int len;
    node* head;
    node* tail;
};

linked_list::linked_list()
{
    len = 0;
    head = new node;
    head->value = NULL;
    head->next = NULL;
    tail = head;
}

linked_list::~linked_list()
{
    while(head->next != NULL){
        node* temp = (head->next)->next;
        delete (head->next);
        head->next = temp;
    }
    delete head;

}

int linked_list::getlen(){
    return len;
}

void linked_list::append(int* value){
    node* temp = new node;
    temp->value = value;
    temp->next = NULL;

    tail->next = temp;
    tail = temp;
    len++;
}

bool linked_list::check_equal(int* new_value){
    node* now = head->next;
    while(now != NULL){
        int count = 0;
        for(int i = 0; i < 26; ++i){
            if(now->value[i] == new_value[i]){
                count++;
            }
        }
        if(count == 26) return 1;
      	now = now->next;
    }
    return 0;
}


int main(){
    int n;
    int k;
    scanf("%d", &n);
    getchar();
    scanf("%d", &k);
    char type_c[n];
    /* for(int i = 0; i < n; ++i){
        cin >> type_c[i];
    }*/
    scanf("%s", type_c);
    //printf("test %c\n", type_c[0]);

    int type[n];
    for(int i = 0; i < n; ++i){
        //printf("char %c\n", type_c[i]);
        type[i] = int(type_c[i]);
    }

    //printf("type %d\n", type[0]);
    int vector[n][26] = {{0}};
    for(int i = 0; i < k; ++i){
        vector[0][type[i] - 97] += 1;  // a represent 97
        //printf("check %d\n", type[i]);
        //printf("there %d\n", vector[0][type[i] - 97]);
    }

    /*for(int i = 0; i < 3; ++i){
        printf("%d\n", vector[0][i]);
    }*/
    for(int i = 1; i <= n - k; ++i){
        for(int j = 0; j < 26; ++j){
            vector[i][j] = vector[i - 1][j];
        }
        vector[i][type[i-1] - 97] -= 1;
        vector[i][type[i+k-1] - 97] += 1;
    }

    /*for(int j = 0; j < n; ++j){
        for(int i = 0; i < 3; ++i){
            printf("%d\n", vector[j][i]);
        }

    }*/

    //long long int hash_value[n];   
    //long long int* hash_value = new long long int[n - k + 1];
  	int result = 0;

    linked_list *hash_value = new linked_list[mod];
    for(int i = 0; i < n - k + 1; ++i){
        long int value = hash_function(vector[i], 26);
        if(hash_value[value].check_equal(vector[i]) == 0){
            hash_value[value].append(vector[i]);
          	result++;
        }
        //printf("hash %lld\n", hash_value[i]);
    }

    /*int result = 0;
    for(int j = 0; j < mod; ++j){
        result += hash_value[j].getlen();
    }*/
    /*memset(flag, 0, mod);
    
    int result = 0;
    for(int i = 0; i < n - k + 1; ++i){
        if(flag[hash_value[i]] == 0){
            result += 1;
            flag[hash_value[i]] = 1;
        }
    }

    printf("%d\n", result);
    delete[] flag;
    delete[] hash_value;*/

    printf("%d\n", result);
    delete[] hash_value;
    return 0;
}