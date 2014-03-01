"""
make a gifti compatible with connectome workbench
"""
import numpy

def wbify_gifti(input):

    f=open(input)
    output=input.replace('.func','_fixed.func',1)
    l=f.readlines()
    f.close()
    # fix endian
    data_start=[]
    data_end=[]
    for i in range(len(l)):
        if l[i].find('GIFTI_ENDIAN_LITTLE')>-1:
#            print l[i]
            l[i]=l[i].replace('GIFTI_ENDIAN_LITTLE','LittleEndian')
#            print l[i]
        if l[i].find('<Data>')>-1:
            data_start.append(i)
        if l[i].find('</Data>')>-1:
            data_end.append(i)
    data_start=numpy.array(data_start)
    data_end=numpy.array(data_end)
    
    assert len(data_start)==len(data_end)
    framelen=data_end - data_start
    
    # fix data representation
    for x in range(len(data_start)):
        dataline=''
        for i in range(data_start[x],data_start[x]+framelen[x]+x):
            dataline+=l[data_start[x]].strip()
            del l[data_start[x]]
            data_start[x+1:]-=1
            #data_end[x+1:]-=1
            #print data_start
            #print data_end
        dataline=dataline+'\n'

        l.insert(data_start[x],dataline)
        f=open(output,'w')
        for i in l:
            f.write(i)
        f.close()

