import csv
import itertools
import pandas as pd
#from __future__ import division
#from sklearn.metrics.scorer import _PredictScorer
from math import floor,ceil

import numpy as np

from Demo import ReadFile


class ReadFile:


    def __init__(self):
        self.Data=[]
        self.dataDictionary={}
        self.TrainSample=118
        self.TestSample=28
        self.dictPredicted={}

    def UpdateFile(self):
        r=ReadFile()
        dict=r.FileRead('product_distribution_training_set.txt')
        plist=r.fileReadNormal('key_product_IDs.txt')
        plist.sort()
        tempList=[]
        for x in plist:
            if x!=0:
                tempList.append(dict[x])
        Overall=[sum(i) for i in zip(*tempList)]
        f=open('product_distribution_training_set.txt','a+')
        strngs=''
        for x in Overall:
            strngs=strngs+" "+str(x)
        strngs="0"+" "+strngs
        f.write("\n"+strngs)
        f.close()
        f = open('key_product_IDs.txt', 'a+')
        f.write('\n0')
        f.close()

    def FileRead(self,filename):
        for line in open(filename,'r'):
            self.Data.append(line.strip())

        for data in range(len(self.Data)):
            temp_str=str(self.Data[data].strip())
            temp_result=temp_str.split()
            self.dataDictionary[int(temp_result[0])]=list(map(int,temp_result[1:]))

        return self.dataDictionary

    def fileReadNormal(self,filename):
        self.Data=[]
        for line in open(filename,'r'):
            self.Data.append(line.strip())

        list1=list(map(int,self.Data))
        return list1

    def CalculateValueAB(self):
        r=ReadFile()
        prodQuantity=r.FileRead('product_distribution_training_set.txt')
        Products = r.fileReadNormal('key_product_IDs.txt')
        Products.sort()
        DictCoef = {}
        for prod in prodQuantity:
            PList = prodQuantity[prod]
            Y=PList[2:]
            X1=PList[1:len(PList)-1]
            X2=PList[:len(PList)-2]
            X1Y=[a*b for a,b in zip(X1,Y)]
            X2Y = [a * b for a, b in zip(X2, Y)]
            X1X2=[a*b for a,b in zip(X1,X2)]
            X1X1 = [a * b for a, b in zip(X1, X1)]
            X2X2 = [a * b for a, b in zip(X1, X2)]
            YY=[a*b for a,b in zip(Y,Y)]
            SumX1Y=sum(X1Y)
            sumX2Y=sum(X2Y)
            sumX1X2=sum(X1X2)
            sumX1X1=sum(X1X1)
            summX2X2=sum(X2X2)
            sumX1=sum(X1)
            sumX2=sum(X2)
            sumY=sum(Y)
            sumYY=sum(YY)
            y=max(Y)
            sumx1y=r.CalculateProducts(len(Y),sumX1,sumY,SumX1Y)

            sumx2y=r.CalculateProducts(len(Y),sumX2,sumY,sumX2Y)
            sumx1x2=r.CalculateProducts(len(Y),sumX1,sumX2,sumX1X2)
            sumyy=r.CalculateProducts(len(Y),sumY,sumY,sumYY)
            sumx1x1=r.CalculateProducts(len(Y),sumX1,sumX1,sumX1X1)
            sumx2x2=r.CalculateProducts(len(Y),sumX2,sumX2,summX2X2)


            B1=((sumx2x2*sumx1y)-(sumx1x2*sumx2y))/(((sumx1x1*sumx2x2)-(sumx1x2*sumx1x2)))
            B2=((sumx1x1*sumx2y)-(sumx1x2*sumx1y))/(((sumx1x1*sumx2x2)-(sumx1x2*sumx1x2)))
            Ybar=sum(Y)/(len(Y)*1.0)
            X1bar = sum(X1) / (len(X1) * 1.0)
            X2bar=sum(X2)/(len(X2)*1.0)
            A=Ybar-(B1*X1bar)-(B2*X2bar)
            coefficient=str(A)+","+str(B1)+","+str(B2)
            YPredict=[]
            for i in range(1,len(Y)):
                Yd=A+B1*X1[i]+B2*X2[i]
                if(Yd<0):
                    Yd=0
                YPredict.append(int(np.rint(abs(Yd%y))))

            DictCoef[prod]=coefficient;
            self.dictPredicted[prod]=YPredict

        return DictCoef

    def CalculateProducts(self,N,sumx1,sumy1,sumX1Y1):
        div=(sumx1*sumy1)/(N*1.0)
        finals=sumX1Y1-(div)
        return finals

    def predict(self):
        r=ReadFile()
        wieghtdict=r.CalculateValueAB()
        predictedValues={}
        prodQuantity = r.FileRead('product_distribution_training_set.txt')
        Products=r.fileReadNormal('key_product_IDs.txt')
        Products.sort()
        for x in Products:
            TempList=[]
            listAB=wieghtdict[x].split(',')
            PList = prodQuantity[x]
            Y = PList[2:]
            A=float(listAB[0])
            B1=float(listAB[1])

            B2=float(listAB[2])
            y=max(Y)
            for i in range(1,29,1):
                Yd=A+B1*Y[-1]+B2*Y[-2]
                Y.append(int(np.rint(abs(Yd%y))))
            predictedValues[x]=Y[116:]

            f = open("ARoutput.txt", "w+")
        for x in Products:
            sr=''
            lis = predictedValues[x]
            for y in lis:
                sr=sr+" "+str(y)
            f.write(str(x)+" "+sr+"\n")
        f.close()
        return predictedValues


r=ReadFile()
f=r.UpdateFile()
h=r.CalculateValueAB()
hh=r.predict()
print(hh)
