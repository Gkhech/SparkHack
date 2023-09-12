# Python program to identify
#color in images

def timeConverter(time):
    timeHold = 0
    if time[0] == '8' or time[0] == '9' or time[0 : 2] == '10' or time[0 : 2] == '11' or time[0 : 2] == '12':
        if(time[1].isdigit()):
            # print("\t10 - 12")
            time = time[0 : 5] + ":00"
        else:
            # print("\tin 8 or 9")
            time = "0" + time[0 : 4] + ":00"
        # print(time)
    elif time[0] == '1' or time[0] == '2' or  time[0] == '3' or  time[0] == '4' or  time[0] == '5' or  time[0] == '6' or  time[0] == '7':
        # print("\tin 1 to 7")
        timeHold = int(time[0]) + 12
        time = str(timeHold) + time[1 : 4] + ":00"
        # print(time)
    return time

def addVal(dict, key, className, timeStart, timeEnd):
    if key not in dict:
        dict[key] = []
    dict[key].append(className)
    dict[key].append(timeStart)
    dict[key].append(timeEnd)

classLine = ""
semester = ""

with open("Registration.html", "r") as f:
    for line in f.readlines():
        if "id=\"calendar\"" in line:
            # print(line,"\n")
            classLine = line
        if "\"startDate\": \"" in line:
            # print(line,"\n")
            semester = line[line.find(": \"") + 3 : line.find(",")]

# print(semLine)
# ---------------------------------------- var declarations below ----------------------------------------
min = 0
Day = ""
Time = ""
TimeStart = ""
TimeEnd = ""
counter = 0
className = ""
classes = {}
# ---------------------------------------- var declarations above ----------------------------------------

print(semester)

week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
end = classLine.count("class=\"section-time-details\" href=\"#\">")

while counter < end:
    min = classLine.find("class=\"section-time-details\" href=\"#\">", min) #finds first instance of the this line 
    # print(min) #prints the win
    min += 38
    Day = classLine[min : classLine.find(" ", min)]
    # print(f"Day:*{Day}*")
    Time = classLine[classLine.find(" ", min) + 1: classLine.find("<", min)]
    # print(f"Time:*{Time}*")
    TimeStart = timeConverter(Time)
    TimeEnd = timeConverter(Time[Time.find("- ") + 2 : ])

    className = classLine[classLine.find("</span>", min) + 7 : classLine.find("</a>", min)]
    # print(f"ClassName:*{className}*")
    addVal(classes, Day, className, TimeStart, TimeEnd)
    min = classLine.find("</a>", min)
    counter += 1

print("after run\n")

print(f"Semmy:*{semester}*\n")

for i in week:
    for j in classes[i]:
        print(j)

