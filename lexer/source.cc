int a=3+2i, b=4 , c=2.45e+55;

function int max(int a,int b){
    if ( a>=b ) return a;
    else return b;
}
function double min(int A,int B){
    if ( A<B ) return A;
    else return B;
}

function int main(){
    int a;
    double a_bb;
    double sum_1_to_50 = 1;
    for(int i=1;i<100;i+=1){
        if ( i<50 ) break;
        else sum_1_to_50 += i;
    }
    int k = 0 , s = ((534-23)+423)*23;
    while ( k<40 ) scanf( s );

    int A = 50 , B = 23 , C;
    C = function max(A,B) ;
    print(C);
    print(A+B*C);

    return 0;
}