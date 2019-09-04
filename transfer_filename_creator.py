props=[22,23,24,25,26]

ints=[0.025,0.030,0.035,0.040,0.045,0.050,0.055,0.060]

sets=[]

command='curl https://transfer.sh/('

for prop in props:
    for int_ in ints:
        sets.append([prop,int_])

for parameters in sets:

    # print(parameters)

    p_gain=parameters[0]

    i_gain=parameters[1]

    filename=str(p_gain).replace('.','-')+'_'+str(i_gain).replace('.','-')+'_automated_TRY2.csv'

    addition=filename+','

    command=command+addition

command=command+').zip'

print(command)
