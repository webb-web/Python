##import matplotlib.pyplot as plt
##import numpy as np
##
##def plot9():
##    data = [zero, one, two, three, four, five, six, seven, eight, nine]
##    labels=["zero","one","two","three","four","five","six","seven","eight","nine"]
##    N = len( data )
##    x = np.arange(1, N+1)
##    width = 1
##    bar1 = plt.bar( x, data, width, color="r" )
##    plt.ylabel( 'Number of Occurances' )
##    plt.xticks(x + width/2.0, labels )
##    plt.show()

import numpy.numarray as na
from pylab import *



pifile = open("pi.txt","r")

#read data from file
picontent=pifile.read()

#remove characters that are not digits
pi=[x for x in picontent if x.isdigit()]


zero = 0
one = 0
two = 0
three = 0
four = 0
five = 0
six = 0
seven = 0
eight = 0
nine = 0

a = 0

while a < len(pi):
    if int(pi[a]) == 0:
        zero = zero + 1
#        print "found 0"
    elif int(pi[a]) == 1:
        one = one + 1
    elif int(pi[a]) == 2:
        two = two + 1
    elif int(pi[a]) == 3:
        three = three + 1
    elif int(pi[a]) == 4:
        four = four + 1
    elif int(pi[a]) == 5:
        five = five + 1
    elif int(pi[a]) == 6:
        six = six + 1
    elif int(pi[a]) == 7:
        seven = seven + 1
    elif int(pi[a]) == 8:
        eight = eight + 1
    elif int(pi[a]) == 9:
        nine = nine + 1
    a = a + 1
    
print( "zero %d one %d two %d three %d four %d five %d six %d seven %d eight %d nine %d" % (zero, one, two, three, four, five, six, seven, eight, nine) )

#plot9()
data = [zero, one, two, three, four, five, six, seven, eight, nine]
labels=["zero","one","two","three","four","five","six","seven","eight","nine"]

xlocations = na.array(range(len(data)))+0.5
width = 0.5
bar(xlocations, data, width=width)
yticks(range(0, 20000))
xticks(xlocations+ width/2, labels)
xlim(0, xlocations[-1]+width*2)
title("Average Ratings on the Training Set")
gca().get_xaxis().tick_bottom()
gca().get_yaxis().tick_left()

show()


