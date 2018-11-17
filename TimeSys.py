def first_state(wl): #sorry...
    if  (wl<400):
        SPF.command('pos=6')
        print("SPF is in posiotion 6 Empty")
        spf = 0
    if (wl>=400)&(wl<440):
        SPF.command('pos=1')
        print("SPF is in posiotion 1 Wavlength 450")
        spf = 450
    if (wl>=440)&(wl<490):
        SPF.command('pos=2')
        print("SPF is in posiotion 2 Wavlength 500")
        spf = 500
    if (wl>=490)&(wl<540):
        SPF.command('pos=3')
        print("SPF is in posiotion 3 Wavlength 550")
        spf =550
    if (wl>=540)&(wl<590):
        SPF.command('pos=4')
        print("SPF is in posiotion 4 Wavlength 600")
        spf = 600
    if (wl>=590)&(wl<640):
        SPF.command('pos=5')
        print("SPF is in posiotion 5 Wavlength 650")
        spf = 650
    if (wl>=640):
        SPF.command('pos=6')
        print("SPF is in posiotion 6 Empty")
        spf = 0
        
    if  (wl<350):
        LPF.command('pos=6')
        print("LPF is in posiotion 6 Empty")
        lpf = 0
    if (wl>=350)&(wl<400):
        LPF.command('pos=1')
        print("LPF is in posiotion 1 Wavlength  400")
        lpf = 400
    if (wl>=400)&(wl<450):
        LPF.command('pos=2')
        print("LPF is in posiotion 2 Wavlength 450")
        lpf = 450
    if (wl>=450)&(wl<500):
        LPF.command('pos=3')
        print("LPF is in posiotion 3 Wavlength 500")
        lpf = 500
    if (wl>=500)&(wl<550):
        LPF.command('pos=4')
        print("LPF is in posiotion 4 Wavlength  550")
        lpf = 550
    if (wl>=550)&(wl<600):
        LPF.command('pos=5')
        print("LPF is in posiotion 5 Wavlength  600")
        lpf=600
    if (wl>=600):
        LPF.command('pos=6')
        print("LPF is in posiotion 6 Empty") 
        lpf = 0
    return spf ,lpf

def second_state(wl): #sorry...
    if  (wl<400):
        SPF.command('pos=6')
        print("SPF is in posiotion 6 Empty")
        spf = 0
    if (wl>=400)&(wl<440):
        SPF.command('pos=1')
        print("SPF is in posiotion 1 Wavlength 450")
        spf = 450
    if (wl>=440)&(wl<490):
        SPF.command('pos=2')
        print("SPF is in posiotion 2 Wavlength 500")
        spf = 500
    if (wl>=490)&(wl<540):
        SPF.command('pos=3')
        print("SPF is in posiotion 3 Wavlength 550")
        spf =550
    if (wl>=540)&(wl<590):
        SPF.command('pos=4')
        print("SPF is in posiotion 4 Wavlength 600")
        spf = 600
    if (wl>=590)&(wl<640):
        SPF.command('pos=5')
        print("SPF is in posiotion 5 Wavlength 650")
        spf = 650
    if (wl>=640):
        SPF.command('pos=6')
        print("SPF is in posiotion 6 Empty")
        spf = 0
    LPF.command('pos=2')
    print("LPF is in posiotion 2 Wavlength 450")
    lpf = 450
    return spf ,lpf

def set_spectro_grating(num):
    ser7.read(150) # empty buffer
    j = 1
    if num == 1:
        ser7.write(b'SetGrating\r')
        ser7.write(b'1\r')
        time.sleep(0.1)
        while(ser7.read(150)!=b'spectro grating set to 1\r\n' and j< 30):
            time.sleep(1)
            j = j + 1
        if j==30:
            print("error: Andor timed out")
            return 0
        print("spectro grating 1 is set", f" - took {j} iteration with 1 s sleep")
    if num == 2:
        ser7.write(b'SetGrating\r')
        ser7.write(b'2\r')
        time.sleep(0.1)
        while(ser7.read(150)!=b'spectro grating set to 2\r\n' and j< 30):
            time.sleep(0.5)
            j = j+1
    if j==30:
        print("error: Andor timed out")
        return 0
    print("spectro grating 2 is set", f" -  took {j} iteration with 1 s sleep")
    return 0

def set_up(wl,state):
    if state == "regular_state":
        spf,lpf = first_state(wl)
        set_spectro_grating(2)
        spectro_grating = 2
        setwavlength(wl + 100)
        spectro_center_wl = wl + 100
    if state == "first_state":
        spf,lpf = first_state(wl)
        set_spectro_grating(1)
        spectro_grating = 1
        setwavlength(wl + 100)
        spectro_center_wl = wl + 100
    if state == "second_state":
        spf,lpf = first_state(wl)
        set_spectro_grating(2)
        spectro_grating = 2
        setwavlength(700)
        spectro_center_wl = 700
    if state == "third_state":
        spf,lpf = second_state(wl)
        set_spectro_grating(2)
        spectro_grating = 2
        setwavlength(700)
        spectro_center_wl = 700
    return spf,lpf,spectro_grating,spectro_center_wl

def set_exposure_time(s):
    print(f'change exposure time to {s} seconds')
    ser7.read(150) # empty buffer
    j = 1
    ser7.write(b'SetExposureTime\r')
    ser7.write(str(s).encode() + b'\r')
    while(ser7.read(150)!=b'Exposure time set to '+str(s).encode()+b'\r\n' and j< 30):
        time.sleep(1)
        j = j + 1
    if j==30:
        print("error: Andor timed out")
        return 0
    print(f'Exposure time set to {s} seconds', f" - took {j} iteration with 1 s sleep")
    return 0

def save_ascii_file(ID, wl, crystal, exposuretime ,measurment_number,date,t):
    print("saving data")
    j = 1
    ser7.write(b'Save\r')
    path = b'C:\Users\Physics\Documents\CrystalScans\\'+crystal.encode()+b"\\"+b'ID_'+ID.encode()+b"\\"+b"Rawdata\\"+ measurment_number.encode()+b"_"+date.encode()+t.encode()+b"_"+b'_ExWl_'+str(wl).encode()+ b'_exposuretime_'+str(exposuretime).encode()+b'.asc\r'
    ser7.write(path)
    while(ser7.read(150)!=b'Saved ascii file in '+path+b'\n' and j< 30):
        time.sleep(0.5)
        j = j + 1
    if j==30:
        print("error: Andor timed out, problems with saving ascii")
        return 0
    print(b'Saved ascii file in '+path, f" - took {j} iteration with 0.5 s sleep")
    return 0

def take_measurement(ID, wl, crystal, exposuretime ,measurment_number):
    now = datetime.datetime.now()
    date = str(now.day)+str(now.month)+str(now.year-2000)
    t = "h"+str(now.hour)+"m"+str(now.minute)
    power =[]
    ser7.write(b'Run\r') 
    while(ser7.read(150)!=b'Done\r\n'):
        power.append(pm.measure_power(wl))
    print(f'power: {np.mean(power)}, std:{np.std(power)}, # samples: {len(power)}')
    save_ascii_file(ID, wl, crystal, exposuretime ,measurment_number,date,t)
    ser7.read(150)
    return np.mean(power), np.std(power), float(len(power)),t

def measurment(crystal ,measurment_number, ID, wl):
    power,std,num,t = [],[],[],[]
    measurment_number = measurment_number +1
    print("")
    print("----------taking measurment")
    measurment_numbert = "{0:0=3d}".format(measurment_number)   
    print(f'mesurment number {measurment_numbert}')
    set_exposure_time(10)
    A,B,C,D= take_measurement(ID, wl, crystal, 10 ,measurment_numbert)
    power.append(A)
    std.append(B)
    num.append(C)
    t.append(D)
    exposure_t = [10]
    j=0
    click = 1 
    while (j < 10):
        j=j+1
        print("")
        print("----------taking measurment")
        measurment_number = measurment_number +1
        measurment_numbert = "{0:0=3d}".format(measurment_number)   
        print(f'mesurment number {measurment_numbert}')
        if click == 1:
            set_exposure_time(1)
            click = 0
        A,B,C,D = take_measurement(ID, wl, crystal, 1 ,measurment_numbert)
        power.append(A)
        std.append(B)
        num.append(C)
        t.append(D)
        exposure_t.append(1)
    t.extend(exposure_t)
    num.extend(t)
    std.extend(num)
    power.extend(std)
    return power,measurment_number


def first_3chars(x):
    return(x[:3])
def create_data_fram(data, crystal , ID, date,set_measurments):
    columns=["# mesurment","ex_wl","spectro_center_wl",'grating','spf','lpf','lpf2',"av_power","std_power","num_power",'time_taken',"ex_time","em_wl","counts"]
    col = len(columns)-2
    click = 1
    n = int(len(data)/(set_measurments*col))
    data = np.array(data).reshape(col*n,set_measurments)
    data_neat = []
    for i in range(col):
        temp = data[i::col,:]
        data_neat = np.append(data_neat,temp)
    data_neat = data_neat.reshape(col,set_measurments*n).T
    path =r"C:\Users\Physics\Documents\CrystalScans\\"+crystal+r'\\ID_'+ID+r"\Rawdata\\"
    file_list = os.listdir(path)
    M = []
    for f, d in zip(sorted(file_list, key = first_3chars)  ,data_neat) :
        print(d)
        wl, count = np.genfromtxt(path+f,skip_footer=28,delimiter = "\t").T
        d = np.array(list(d)*1600).reshape(1600,col).T
        d = np.vstack((d,wl))
        d = np.vstack((d,count))
        if click == 1:
            click =0
            M = d.T
            continue
        M = np.hstack((M,d.T))
    print(n)
    Result = pd.DataFrame(M.reshape(1600*set_measurments*n,col+2), columns=["# mesurment","ex_wl","spectro_center_wl",'grating','spf','lpf','lpf2',"av_power",
                                                          "std_power","num_power",'time_taken',"ex_time","em_wl","counts"])
    Result.to_csv(r"C:\Users\Physics\Documents\CrystalScans\\"+crystal+r'\ID_'+ID+r"\\Scan.csv")              
    return Result


def find_ID():
    id_list =[]
    for name in os.listdir(r"C:\Users\Physics\Documents\CrystalScans\\"):
        path = r"C:\Users\Physics\Documents\CrystalScans\\"+ name
        if os.path.isdir(path):
            id_list.extend(os.listdir(path))
    id_list = [i for i in id_list if i[:3]=="ID_" and len(i)==6]
    try:
        ID = int(max(id_list)[3:])
    except:
        ID = 0
    ID = "{0:0=3d}".format(ID+1)
    print(f"measurment ID_{ID}")
    return ID
    
def creatfiles(crystal,ID):
    try:
        os.mkdir(r"C:\Users\Physics\Documents\CrystalScans\\"+crystal+r"\\")
    except:
        pass
    try:
        os.mkdir(r"C:\Users\Physics\Documents\CrystalScans\\"+crystal+r"\\"+"ID_"+ID+r"\\")
    except:
        pass
    try:
        os.mkdir(r"C:\Users\Physics\Documents\CrystalScans\\"+crystal+r"\\"+"ID_"+ID+r"\Rawdata\\")
    except:
        pass
    return 0 


def setwavlength(wl):
    print(f"{str(datetime.datetime.now())} : Setting spectro center wavelngth")
    ser7.read(150)
    ser7.write(b'SetWavelength\r')
    ser7.write(str(wl).encode()+b'\r')
    A = ser7.read(150)
    j=0
    while(A==b""and j<30):
        time.sleep(0.5)
        j = j + 1
        A = ser7.read(150)
    if j>30:
        print("Andor time out no wavelength set")
    print("Andor:",A, f" - took {j} iteration with 0.5 s sleep")
    return 0

def calibration_scan(crystal):
    now = datetime.datetime.now()
    date = str(now.day)+str(now.month)+str(now.year-2000)
    t = "h"+str(now.hour)+"m"+str(now.minute)
    ser7.read(150) # Empty Andor Buffer
    c = "SP_B1_001"
    data= []
    print(f"--------------------------------------Scan of {c}")
    ID = find_ID()
    creatfiles(c,ID)
    print("--------------------Defining intial parameters")
    setGrating(ser1, 2) 
    lpf = 0
    lpf2 = 0
    motor.write(down_position)
    print("no LPF before sample")
    data = []
    measurment_number = 0
    print("------------------------------------------------------------------------------------") 
    goto(ser1,450)
    print("---------------------------------Excitation wl: ", 450)
    spf,lpf,spectro_grating,spectro_center_wl = set_up(450,"regular_state")
    set_exposure_time(10)
    start = time.time()
    while((time.time() -start)/(60*60.)<1.):
        measurment_number = measurment_number +1
        print("")
        print("----------taking measurment")
        measurment_numbert = "{0:0=3d}".format(measurment_number)   
        print(f'mesurment number {measurment_numbert}')
        print((time.time() -start)/60.)
        power = []
        print((time.time()-start)/60.)
        A,B,C,D= take_measurement(ID, 450, c, 10 ,measurment_numbert)
        power.extend([A,B,C,D,10])
        data.extend([measurment_number])          
        data.extend([450,spectro_center_wl,spectro_grating,spf,lpf,lpf2])
        data.extend(power) 
        print((time.time() -start)/60.)
        with open(r"C:\Users\Physics\Documents\CrystalScans\\"+c+r"\\ID_"+ID+r"\back_up.txt", "wb") as fp:
            pickle.dump(data, fp)
        time.sleep(60.)
    print(data)
    print(c, ID, date)
    df = create_data_fram(data, c, ID, date,1)
    return df
