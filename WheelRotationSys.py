motor_wheel = apt.Motor(27503140)
def save_ascii_file(ID, wl, crystal, exposuretime ,measurment_number,date,t,d_name):
    print("saving data")
    j = 1
    ser7.write(b'Save\r')
    path = b'C:\Users\Physics\Documents\CrystalScans\\'+crystal.encode()+b"\\"+b'ID_'+ID.encode()+b"\\"+b"Rawdata\\"+ measurment_number.encode()+b"_"+date.encode()+t.encode()+b"_"+b'_ExWl_'+str(wl).encode()+ b'_exposuretime_'+str(exposuretime).encode()+b'_'+d_name.encode()+b'.asc\r'
    ser7.write(path)
    while(ser7.read(150)!=b'Saved ascii file in '+path+b'\n' and j< 30):
        time.sleep(0.5)
        j = j + 1
    if j==30:
        print("error: Andor timed out, problems with saving ascii")
        return 0
    print(b'Saved ascii file in '+path, f" - took {j} iteration with 0.5 s sleep")
    return 0

def take_measurement(ID, wl, crystal, exposuretime ,measurment_number,d_name):
   
    now = datetime.datetime.now()
    date = str(now.day)+str(now.month)+str(now.year-2000)
    t = "h"+str(now.hour)+"m"+str(now.minute)
    power =[]
    ser7.write(b'Run\r') 
    while(ser7.read(150)!=b'Done\r\n'):
        power.append(pm.measure_power(wl))
    print(f'power: {np.mean(power)}, std:{np.std(power)}, # samples: {len(power)}')
    save_ascii_file(ID, wl, crystal, exposuretime ,measurment_number,date,t,d_name)
    ser7.read(150)
    return np.mean(power), np.std(power), float(len(power)),t


def rotation_sys_check(c, repeats=5, direction=1, mode='half_turn'):
    start_pos = motor_wheel.position
    print(f'started at {start_pos}')
    now = datetime.datetime.now()
    date = str(now.day)+str(now.month)+str(now.year-2000)
    t = "h"+str(now.hour)+"m"+str(now.minute)
    ser7.read(150) # Empty Andor Buffer
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
    for _ in range(repeats):
        measurment_number = measurment_number +1
        print("")
        print("----------taking measurment")
        measurment_numbert = "{0:0=3d}".format(measurment_number)   
        print(f'mesurment number {measurment_numbert}')
        print((time.time() -start)/60.)
        power = []
        print((time.time()-start)/60.)
        d_name = {1:"up",-1:"down"}[direction]
        A,B,C,D= take_measurement(ID, 450, c, 10 ,measurment_numbert,d_name)
        power.extend([A,B,C,D,10])
        data.extend([measurment_number])          
        data.extend([450,spectro_center_wl,spectro_grating,spf,lpf,lpf2])
        data.extend(power) 
        print((time.time() -start)/60.)
        with open(r"C:\Users\Physics\Documents\CrystalScans\\"+c+r"\\ID_"+ID+r"\back_up.txt", "wb") as fp:
            pickle.dump(data, fp)
        
        if mode == 'abs':
            pos = motor_wheel.position
            for i in range(1,13):
                print(f" moving to {pos + i*direction*30}")
                motor_wheel.move_to(pos + i*direction*30, blocking=True)
                print(f"    at pos {motor_wheel.position-pos - i*direction*30}")
                time.sleep(0.2)
                
        elif mode=='abs_abs':
            for i in range(1,13):
                pos = start_pos + i*direction*30
                print(f" moving to {pos}")
                motor_wheel.move_to(pos , blocking=True)
                current = motor_wheel.position
                print(f"at pos {current} diff : {current-pos}")
                time.sleep(0.2)
                
        elif mode=='half_turn':
            for _ in range(6):
                motor_wheel.move_by(direction*30, blocking=True)
                time.sleep(.5)
            for _ in range(6):
                motor_wheel.move_by(-direction*30, blocking=True)
                time.sleep(.5)
                
        elif mode=='traceback':
            for _ in range(13):
                motor_wheel.move_by(direction*30, blocking=True)
                time.sleep(.5)
                print(f"    at pos {motor_wheel.position}")
            motor_wheel.move_by(-direction*30, blocking=True)
            time.sleep(.5)
            print(f"    at pos {motor_wheel.position}")
        else:
            for _ in range(12):
                motor_wheel.move_by(direction*30, blocking=True)
                time.sleep(10)
    #        time.sleep(10.)

    print(data)
    print(c, ID, date)
    df = create_data_fram(data, c, ID, date,1)
    return df
df = pd.DataFrame.from_csv(r"C:\Users\Physics\Documents\CrystalScans\SP_B1_001\ID_001\Scan.csv")
#print(df.sort_values(by=["# mesurment"]))
df.em_wl=pd.to_numeric(df.em_wl)
df.counts=pd.to_numeric(df.counts)
df.av_power=pd.to_numeric(df.av_power)

fig, ax = plt.subplots()
df["counts"] = df["counts"]/df["av_power"]
df.groupby("# mesurment").plot(x = "em_wl",y ="counts", ax=ax)
ax.get_legend().remove()

fig, ax2 = plt.subplots()
m = df[np.logical_and(740>df["em_wl"] , df["em_wl"]>715)]
m.groupby("# mesurment").plot(x = "em_wl",y ="counts", ax=ax2)
ax2.get_legend().remove()

#fig, ax4 = plt.subplots()
#df.plot(x = "# mesurment",y ="av_power", ax=ax4)
#ax4.get_legend().remove()

fig, ax3 = plt.subplots()
m.groupby("# mesurment")["counts"].mean().plot(ax=ax3)
H = m.groupby("# mesurment")["counts"].mean().mean()
K = m.groupby("# mesurment")["counts"].mean().std()
print(f"mean of range {H} ,the std is {K},ratio is {K/H}")

