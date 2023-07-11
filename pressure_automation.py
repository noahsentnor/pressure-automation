# notes: 
# make a section of code that checks the average change in pressure is the amount we want
# make something that detects idling pressure. if pressure is idling, continue to a safe termination of system and display message

from tkinter import *
from tkinter import ttk
import u3
import time
import random

def open_valve():
    print("valve opened")
    # d.setFIOState(4, state = 1)
    time.sleep(time_between_readings_in_seconds)

def close_valve():
    print("valve closed")
    # d.setFIOState(4, state = 0)
    time.sleep(time_between_readings_in_seconds)

def readTransducer(counter):
    # return float(input("Enter the pressure (this will become a reading from the pressure transducer): "))
    
    instantaneous_pressure = counter - random.randrange(1,11)#*(random.randrange(1,11))
    if instantaneous_pressure < 0:
        instantaneous_pressure = 0
    return instantaneous_pressure
    
    # return counter*10
    
    # pressure = d.getAIN(0) * 20000
    # return pressure

def drawdownFirstStep(instantaneous_pressure, constant_pressure_counter1, goal_pressure):
    if constant_pressure_counter1 >= 10:
        if instantaneous_pressure+5 >= goal_pressure and instantaneous_pressure-5 <= goal_pressure:
            return False
    return True

def drawdownSecondStep(back_to_initial):
    if back_to_initial >= 5:
        print("System terminating.")
        return False
    return True
# def drawdownSecondStep(instantaneous_pressure, constant_pressure_counter1, initial_pressure):
#     if constant_pressure_counter1 >= 10 or instantaneous_pressure-10 > initial_pressure:
#         if (instantaneous_pressure+5 >= initial_pressure and instantaneous_pressure-5 <= initial_pressure) or (instantaneous_pressure-10 > initial_pressure):
#             print("System terminating.")
#             return False
#     return True

def find_average_pressure(average_pressure_array):
    total = 0
    length1 = len(average_pressure_array)
    if length1 <= 1:
        return 0
    pressure_difference_array = []
    for i in range(1,length1):
        pressure_difference_array.append(average_pressure_array[i-1] - average_pressure_array[i])
    length2 = len(pressure_difference_array)
    for j in range(length2):
        total += pressure_difference_array[j]
    print(average_pressure_array,pressure_difference_array)
    return total / length2

# d = u3.U3()

root = Tk()
root.title("Pressure Automation GUI")
root.geometry("500x500")
root.grid()
frm = ttk.Frame(root)
frm.grid(column=0, row=0)

label1 = Label(frm, text="Pressure you are trying to reach (Pa): ")
label1.pack(pady=5)

pressure_entry = Entry(frm, width=20)
pressure_entry.pack(pady = 5)
pressure_entry.focus_set()

def store_pressure_goal():
    global pressure_entry
    string = int(pressure_entry.get())
    return string

ttk.Button(frm, text= "Enter", width= 20, command=store_pressure_goal).pack(pady=5)


# while the system is running:
time_between_readings_in_seconds = 0.1
pressure_current = 100
rate_of_change_of_pressure = (5000/60) # 5000 Pa/min, 83.3 Pa/sec
pressure_goal_in_Pa = int(input("Enter the pressure you are trying to reach: "))
counter = 100
pressure_initial = readTransducer(counter)
constant_pressure_counter = 0
redundant_constant_pressure = False
back_to_initial_pressure_counter = 0
pressure_goal_reached_counter = 0
average_pressure = []
while counter > 0 and drawdownFirstStep(pressure_current, constant_pressure_counter, pressure_goal_in_Pa) and pressure_goal_reached_counter <= 3:
    pressure_past = pressure_current
    # read pressure, set to pressure_current
    pressure_current = readTransducer(counter)
    average_pressure.append(pressure_current)
    if len(average_pressure) > 1/time_between_readings_in_seconds:
        average_pressure.pop(0)
    print(pressure_current)
    print(find_average_pressure(average_pressure))
    if find_average_pressure(average_pressure) > (rate_of_change_of_pressure * time_between_readings_in_seconds):
        print("Average drawdown rate is too high. Making adjustments.")
        open_valve()
        continue

    if pressure_current < pressure_past:
        redundant_constant_pressure = False
        print("pressure going down")
        if pressure_current+5 >= pressure_goal_in_Pa and pressure_current-5 <= pressure_goal_in_Pa: #increment counter, when counter gets to a certain number (prevents fluke) --> initiate next phase (in the drawdown case the next phase will be something related to conducting tests)
            print("pressure has reached", pressure_goal_in_Pa)
            pressure_goal_reached_counter += 1
            if pressure_current < pressure_goal_in_Pa:
                open_valve()
            else:
                close_valve()
        elif pressure_current > pressure_goal_in_Pa:
            if pressure_current + (rate_of_change_of_pressure * time_between_readings_in_seconds) < pressure_past:
                print("too fast")
                open_valve()
            else:
                print("too slow or just right")
                close_valve()
        else: # pressure is less than goal
            print("less than goal!")
            open_valve()
            # counter +=1
    elif pressure_current > pressure_past:
        redundant_constant_pressure = False
        print("pressure going up")
        if pressure_current+5 >= pressure_goal_in_Pa and pressure_current-5 <= pressure_goal_in_Pa:
            print("pressure has reached", pressure_goal_in_Pa)
            pressure_goal_reached_counter += 1
            if pressure_current < pressure_goal_in_Pa:
                open_valve()
            else:
                close_valve()
        elif pressure_current < pressure_goal_in_Pa:
            if pressure_current - (rate_of_change_of_pressure * time_between_readings_in_seconds) > pressure_past:
                print("too fast")
                open_valve()
            else:
                print("too slow or just right")
                close_valve()
        else: # pressure is greater than goal
            print("greater than goal")
            close_valve()
    else:
        print("pressure did not change") #could increase counter to identify how many times this occurred in a row and take action accordingly
        if pressure_current+5 >= pressure_goal_in_Pa and pressure_current-5 <= pressure_goal_in_Pa:
            print("pressure has reached", pressure_goal_in_Pa)
            pressure_goal_reached_counter += 1
            if pressure_current < pressure_goal_in_Pa:
                open_valve()
            else:
                close_valve()
        elif pressure_current < pressure_goal_in_Pa:
            open_valve()
        else:
            close_valve()
            
        if redundant_constant_pressure == False:
            constant_pressure_counter = 1
            redundant_constant_pressure = True
        else:
            constant_pressure_counter += 1

    counter -= 1
# ******************************************************************************************************************************************************************************************
print("exiting drawdown phase, proceeding to drawup phase")
# ******************************************************************************************************************************************************************************************
# drawing the pressure back up after testing is completed
constant_pressure_counter = 0
while counter < 1100 and drawdownSecondStep(back_to_initial_pressure_counter): #(pressure_current, constant_pressure_counter, pressure_initial):
    pressure_past = pressure_current
    # read pressure, set to pressure_current
    pressure_current = readTransducer(counter)
    print(pressure_current)
    if pressure_current < pressure_past:
        redundant_constant_pressure = False
        print("pressure going down")
        open_valve()
        if pressure_current+5 >= pressure_initial and pressure_current-5 <= pressure_initial:
            print("pressure has reached", pressure_initial)
            back_to_initial_pressure_counter += 1
    elif pressure_current > pressure_past:
        redundant_constant_pressure = False
        print("pressure going up")
        if pressure_current+5 >= pressure_initial and pressure_current-5 <= pressure_initial: # will never be exact same reading as initial reading, this is a safe value to open valve and terminate system
            open_valve()
            print("pressure has reached", pressure_initial)
            back_to_initial_pressure_counter += 1
        else:
            if pressure_current - (rate_of_change_of_pressure * time_between_readings_in_seconds) > pressure_past:
                print("too fast")
                close_valve()
            else:
                print("too slow or just right")
                open_valve()
    else: # will realistically almost never happen
        print("pressure did not change") #could increase counter to identify how many times this occurred in a row and take action accordingly
        open_valve()
        if pressure_current+5 >= pressure_initial and pressure_current-5 <= pressure_initial: # will never be exact same reading as initial reading, this is a safe value to open valve and terminate system
            print("pressure has reached", pressure_initial)
            back_to_initial_pressure_counter += 1

        if redundant_constant_pressure == False:
            constant_pressure_counter = 1
            redundant_constant_pressure = True
        else:
            constant_pressure_counter += 1
    counter += 1
    if constant_pressure_counter == 10:
        print("Pressure in chamber is back to pressure outside chamber.\nPlease turn off vacuum pump and open manual valve before shutting off automation system. Solenoid valve will close once system is terminated.")


root.mainloop()