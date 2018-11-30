
# coding: utf-8

# In[1]:

#!/usr/bin/env python

# Copyright (C) 2018 Sai Raghavendra Maddhuri, Genki Terashi, Daisuke Kihara, and Purdue University.
# This file is a part of Emap2sec package with -
# Reference: Maddhuri S,Terashi G, Kihara D. Protein Secondary Structure Detection in Intermediate Resolution Cryo-Electron Microscopy Maps Using Deep Learning. In submission (2018).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#Run Inst.s
#python dataset.py test_out out.dssp outputD


import sys
import numpy as np

dataFile = sys.argv[1];
#labelFile = sys.argv[2];
strideFile = sys.argv[2];
outputFile = sys.argv[3];
factor=int(sys.argv[5])
fil1 = open(dataFile);
#fil2 = open(labelFile);
fil3 = open(outputFile,'w');    
fil4 = open(strideFile)
lines1 = fil1.readlines();
#lines1 = lines1[1:len(lines1)];
print(len(lines1));

#lines2 = fil2.readlines();
#lines2 = lines2[28:len(lines2)];
lines4 = fil4.readlines();
labelArray = [];
labelArray1 = [];
j=0;
acount=0
bcount=0
ccount=0

for line in lines4:
    if(line.split()[0]=='ASG'):
        if(line.split()[5]=='H' or line.split()[5]=='G' or line.split()[5]=='I'):
            labelArray1.append(2);
            acount+=1
        elif(line.split()[5]=='B' or line.split()[5]=='E'):
            labelArray1.append(1);
            bcount+=1
        else:
            labelArray1.append(0);
            ccount+=1
#        ccount+=1
print(np.array(labelArray))
print(np.array(labelArray1))
print(np.array_equal(np.array(labelArray),np.array(labelArray1)))
print("id:"+sys.argv[4])
print("alhpa : %d, beta : %d, none : %d\n"% (acount,bcount,ccount))

count=0
coords=[]
for line in lines1:
    if(line.rstrip()==''):
        continue
    elif(line.startswith("-2") or line.startswith('#C: Res= -2')):
        continue   
    elif(line.startswith('#C:')):
        equ = line.split('=')
        coords = equ[len(equ)-1].split(' ')[1:4]
        #print(coords)
        continue
 
 
    if(line.startswith("-1")):
        fil3.write(str(int(int(coords[0])/factor))+","+str(int(int(coords[1])/factor))+","+str(int(int(coords[2].rstrip())/factor))+','+line)
        #fil3.write(line)
        #fil3.write('\n')
        continue    

    elif(line.startswith('#Base') or line.startswith('#Steps')):
        continue    

    elif(line.startswith("#Voxel")):
        print('!!!!!!!!!1here!!!!!!!!!!!!!!!!!')    
        fil3.write(line.split()[2]+","+line.split()[3]+","+line.split()[4])
        fil3.write('\n')
        continue
    elif(line.startswith("#dmax")):
        continue    

    if(count==1):
        print(line)
        #print(labelArray1[(int(line.split(',')[0])-1)])    
    li = line.split(',');
    flag=0;
    #print(len(labelArray1))
    for i in li:
        if(flag==0):
            #print(int(i)-1);
            lbs = i.split(';')
            ones=[0,0,0]
            for j in lbs:
                #print(lbs)
               	#print((int(j)-1))
                if((int(j)-1)>=len(labelArray1)):
                    continue
                ones[labelArray1[(int(j)-1)]]=1
                if(ones==[1,1,1]):
                    break
            if(np.sum(np.array(ones))==0):
                label="-1" 
            else:           
                labelA = [str(k) for k,l in enumerate(ones) if l!=0]
                label = ':'.join(labelA)

            fil3.write(str(int(int(coords[0])/factor))+","+str(int(int(coords[1])/factor))+","+str(int(int(coords[2].rstrip())/factor))+',')
            fil3.write(label)
            #print(label);
            flag=1;

        else:
            #print(i);
            fil3.write(',');
            fil3.write(i);
    #fil3.write('\n');
    count+=1
