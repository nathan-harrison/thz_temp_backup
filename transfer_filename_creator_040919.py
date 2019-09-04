commands=[]

props=[24]

ints=[0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020,0.021,0.022,0.023,0.024,0.025,0.026,0.027,0.028,0.029,0.030,0.031,0.032,0.033,0.034,0.035]

sets=[]

for prop in props:
    for int_ in ints:
        sets.append([prop,int_])

for parameters in sets:

    # print(parameters)

    p_gain=parameters[0]

    i_gain=parameters[1]

    filename=str(p_gain).replace('.','-')+'_'+str(i_gain).replace('.','-')+'_automated_TRY3.csv'

    command="curl --upload-file ./"+filename+" https://transfer.sh/"+filename

    commands.append(command)

for each in commands:
    print(each+"\n \n")
