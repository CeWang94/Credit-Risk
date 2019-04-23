import math
from scipy.stats import norm
#########Merton Model#########
#Risk free rate
r=0.05
#Time
T=1
#Debt
B=135
#Stock price
S0=100
#Stock volatility
sigma_s=0.3
#discount
discount=math.exp(-r*T)
#Start point of V0 and sigma_v
V0=150
sigma_v=0.5
def d1(V0,sigma_v):
    part1=math.log(V0/B)
    part2=(r+sigma_v*sigma_v*0.5)*T
    part3=sigma_v*math.sqrt(T)
    return (part1+part2)/part3
def d2(V0,sigma_v):
    return d1(V0,sigma_v)-sigma_v*math.sqrt(T)
def F_square(V0,sigma_v):
    return (V0*norm.cdf(d1(V0,sigma_v))-B*discount*norm.cdf(d2(V0,sigma_v))-S0)**2
def G_square(V0,sigma_v):
    return ((sigma_v/sigma_s)*norm.cdf(d1(V0,sigma_v))*V0-S0)**2
def target(V0,sigma_v):
    return F_square(V0,sigma_v)+G_square(V0,sigma_v)
change_V0=10
change_sigma_v=1
count=0
improvement=10
while improvement>=0.0001:
    stepsize=max((1-0.0001*count),0.0001)
    new_V0=V0-stepsize*(target(V0+0.0005,sigma_v)-target(V0-0.0005,sigma_v))/0.001
    new_sigma_v=sigma_v-stepsize*(target(V0,sigma_v+0.00005)-target(V0,sigma_v-0.00005))/0.0001
    while new_V0<= 0 or new_sigma_v <= 0:
        stepsize=stepsize*0.9
	new_V0=V0-stepsize*(target(V0+0.0005,sigma_v)-target(V0-0.0005,sigma_v))/0.001
        new_sigma_v=sigma_v-stepsize*(target(V0,sigma_v+0.00005)-target(V0,sigma_v-0.00005))/0.0001
    while target(new_V0,new_sigma_v)>target(V0,sigma_v):
        stepsize=stepsize*0.95
        new_V0=V0-stepsize*(target(V0+0.0005,sigma_v)-target(V0-0.0005,sigma_v))/0.001
        new_sigma_v=sigma_v-stepsize*(target(V0,sigma_v+0.00005)-target(V0,sigma_v-0.00005))/0.0001
    improvement=target(V0,sigma_v)-target(new_V0,new_sigma_v)
    V0=new_V0
    sigma_v=new_sigma_v
    print(target(V0,sigma_v))
    count+=1
print(norm.cdf(-d2(V0,sigma_v)))
