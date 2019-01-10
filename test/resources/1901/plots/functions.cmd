# saturating
sig(x)=1.0/(1+exp(-x))
pentan(x)=x>0?tanh(x):0.25*tanh(x)  

# non-saturating
swish(x)=x*sig(x)
maxsig(x)=x>sig(x)?x:sig(x)
cosid(x)=cos(x)-x
minsin(x)=x<sin(x)?x:sin(x)   
arctid(x)=atan(x)**2-x
maxtanh(x)=x>tanh(x)?x:tanh(x)  
lrelu1(x)=x>0?x:0.01*x
lrelu2(x)=x>0?x:0.3*x   

linear(x)=x
elu(x)=x<0?exp(x)-1:x
selu(x)=x<0?1.0507*1.67326*(exp(x)-1):1.0507*x
cube(x)=x**3
relu(x)=x<0?0:x

set grid
set key bottom right

set xzeroaxis lw 4
set yzeroaxis lw 4

plot[-4:4] sig(x) lw 4,pentan(x) lw 4,tanh(x) lw 4 , sin(x) lw 4