# ConditionEventNet
C/E Net generator

This project is aiming at random generates Conditon/Event Net. <br></br>
The original idea is from random network generation theory for complex networks. <br></br>

Output file likes <br></br>
```
event
e1(-3,1)
e2(-3,1)
e3(-1,1)
e4(-4,3)
e5(-4,4)
condition
e1(-3)
e1(-2)
e1(-1)
e1(1)
e2(-3)
e3(-1)
e4(-4)
e4(2)
e5(-4)
e5(1)
e5(3)
e5(4)
edge
e1(-3), e1(-3,1)
e1(-2), e1(-3,1)
e1(-1), e1(-3,1)
e1(-3,1), e1(1)
e2(-3), e2(-3,1)
```

The usage of this project is showed as below
```
   python random_net_generator.py --s 2 --t 4 --c 4 --o output.txt
