from __future__ import print_function


from datetime import date
from datetime import datetime
from datetime import timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


className = "Programming Language Design"
startTimeH = 12
startTimeM = 0
endTimeH = 14
endTimeM = 50
isoformDay = "2023-04-09 10:00:00"
location = "test 6"
classLine = ""
semester = ""

#semObj = date(2023,8,21)
#day1.year = 2023
#day1.month = 8
#day1.day = 21

def mergeDate(dateObj, timeObj):
    dt = dateObj
    tm = timeObj
    combined = datetime.combine(dt, tm)
    #print(combined)
    return combined


def get_date_from_weekday(weekday, start, semObj, timeObj):
    # 0 is monday
    today = semObj
    #print("TODAYS DATE")
    #print(today)
    #print("ITS OUT")
    days_ahead = weekday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    if start > 0:
        #target_date = datetime(today.year, today.month, today.day) +(timeObj)
        target_date = mergeDate(semObj, timeObj)
        #print(target_date)
    else:
        #target_date = datetime(today.year, today.month, today.day) + (timeObj)
        target_date = mergeDate(semObj, timeObj)
        #print(target_date)
    return target_date.isoformat()


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

def dayToInt(day):
    if day in "Monday":
        return 0
    if day in "Tuesday":
        return 1
    if day in "Wednesday":
        return 2
    if day in "Thursday":
        return 3
    if day in "Friday":
        return 4

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def parse(creds):
    with open("Registration.htm", "r") as f:
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
    # there was an extra quote so i removed it
    semester = semester.strip('\"')
    # convert to datetime object
    semObj = datetime.strptime(semester, '%m/%d/%Y').date()
    semObj.isoformat()
    #print(semObj)

    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    end = classLine.count("class=\"section-time-details\" href=\"#\">")
    lastDay = 1
    dayInc = 1
    yesterday = "Monday"
    otherday = ""
    while counter < end:
        min = classLine.find("class=\"section-time-details\" href=\"#\">", min) #finds first instance of the this line 
        #print(min) #prints the win
        min += 38
        Day = classLine[min : classLine.find(" ", min)]
        #print(f"Day:*{Day}*")

        # change to int
        intRepDay = dayToInt(Day)
        currDay = intRepDay
        #print(intRepDay)
        #print("+++++ LOOP +++++")
        #print(currDay)
        #print(lastDay)
        #print("+++++ LOOP END +++++")
        Time = classLine[classLine.find(" ", min) + 1: classLine.find("<", min)]
        
        TimeStart = timeConverter(Time)
        TimeEnd = timeConverter(Time[Time.find("- ") + 2 : ])
        startObj = datetime.strptime(TimeStart, '%H:%M:%S').time()
        startObj.isoformat()
        endObj = datetime.strptime(TimeEnd, '%H:%M:%S').time()
        endObj.isoformat()
        #print(f"Start Time:*{startObj}*")
        #print(f"End Time:*{endObj}*")
        localEnd = get_date_from_weekday(intRepDay, 1, semObj, endObj,)
        localStart = get_date_from_weekday(intRepDay, 0, semObj, startObj)
        #print(localEnd) #2023-08-21T10:50:00
        #print(localStart) #2023-08-21T10:00:00
        #dtoe = datetime.strptime(localEnd, '%y-%m-%dT%H:%M:%S')
        #dtos = datetime.strptime(localStart, '%y-%m-%dT%H:%M:%S')
        
        className = classLine[classLine.find("</span>", min) + 7 : classLine.find("</a>", min)]
        #print(f"ClassName:*{className}*")
        addVal(classes, Day, className, TimeStart, TimeEnd)
        min = classLine.find("</a>", min)
        # createEvent(creds, startDate, endDate, className):
        print(f"Today: {Day}     Yesterday: {yesterday}      otherday: {otherday}")
        if Day != yesterday:
            #print(f"Day:*{Day}*")
            nextDay = 1
            yesterday = Day
            otherday = Day
        elif otherday != Day:
            #print(f"Day:*{Day}*")
            nextDay = 0
            yesterday = Day
            otherday = Day
        else:
            nextDay = 0
        print(f"Day:*{Day}*")
        print(nextDay)
        print(dayToInt(Day))
        createEvent(creds, localStart, localEnd, className, nextDay, dayToInt(Day))
        lastDay = currDay
        counter += 1
    """
    #print("after run\n")
    localClass = ""
    localEnd = TimeStart
    localStart = TimeEnd
    print(f"Semmy:*{semester}*\n")
    iterator = 0
    for i in week:
        #dayToInt(i)
        for j in classes[i]:
            print("")
            print(f"Iteration: {iterator} ")
            if not iterator % 3  and iterator % 2:
                localEnd = get_date_from_weekday(dayToInt(i), 1)
            elif not iterator % 2 and iterator % 3:
                localStart = get_date_from_weekday(dayToInt(i), 0)
            elif not has_numbers(j):
                localClass = j
            print("CURRENT DAY")
            print(i)
            print("INT REP OF DAY")
            print(dayToInt(i))
            print("END")
            print(localEnd)
            print("START")
            print(localStart)
            print("CLASS")
            print(localClass)
            print(f"END OF Iteration: {iterator} ======================")
            iterator += 1
            
            #print(" ")
            #print("START J CONTENT")
            #print(j)
            #print("END J CONTENT")
            #print(" ")
            #createEvent(creds)
            """

def createEvent(creds, startDate, endDate, className, nextDay, dayInc):
    service = build('calendar', 'v3', credentials=creds)

    FA23start = "20230822T170000Z"
    FA23end = "20231213T170000Z"

    recurrenceRule = "RRULE:FREQ=WEEKLY;UNTIL="
    recurrencceForm = recurrenceRule + FA23end

    
    #startprop = tomorrow.isoformat()
    #endprop = (tomorrow + timedelta(hours=1)).isoformat()
    #date_next = str(date) + str(datetime.timedelta(week - 1))
    """
    if nextDay:
        print("NEXT DAY HAPPENS")

        d = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
        dE = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S')
        #d = startDate
        #print(d)
        #print(dE)
        tomorrow = datetime(d.year, d.month, d.day)+timedelta(days = dayInc ,hours = d.hour, minutes = d.minute)
        tomorrowE = datetime(dE.year, dE.month, dE.day)+timedelta(days = dayInc, hours = dE.hour, minutes = dE.minute)
        #print(tomorrow.isoformat())
        #print(tomorrowE.isoformat())
        start = str(tomorrow.isoformat())
        end = str(tomorrowE.isoformat())
        
    else:
        tomorrow = datetime(d.year, d.month, d.day)+timedelta(days = dayInc ,hours = d.hour, minutes = d.minute)
        tomorrowE = datetime(dE.year, dE.month, dE.day)+timedelta(days = dayInc, hours = dE.hour, minutes = dE.minute)
        #print(tomorrow.isoformat())
        #print(tomorrowE.isoformat())
        start = str(tomorrow.isoformat())
        end = str(tomorrowE.isoformat())
        """
    d = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    dE = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S')
    #d = startDate
    #print(d)
    #print(dE)
    tomorrow = datetime(d.year, d.month, d.day)+timedelta(days = dayInc ,hours = d.hour, minutes = d.minute)
    tomorrowE = datetime(dE.year, dE.month, dE.day)+timedelta(days = dayInc, hours = dE.hour, minutes = dE.minute)
    #print(tomorrow.isoformat())
    #print(tomorrowE.isoformat())
    start = str(tomorrow.isoformat())
    end = str(tomorrowE.isoformat())
    #print(startprop)
    #print(endprop)
    #print(start)
    #print(end)

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": className,
            "description": location,
            "start": {"dateTime": start, "timeZone": "America/Chicago"},
            "recurrence":[recurrencceForm],

            "end": {"dateTime": end, "timeZone": "America/Chicago"},
    }).execute()
    print("created event")
    #print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    #print("starts at: ", event_result['start']['dateTime'])
    #print("ends at: ", event_result['end']['dateTime'])

def main():
    """Shows basic usage of the Google Calendar API."""

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    

    try:
        parse(creds)
        #createEvent(creds)

        # Call the Calendar API
        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # events_result = service.events().list(calendarId='primary', timeMin=now,
        #                                      maxResults=10, singleEvents=True,
        #                                      orderBy='startTime').execute()
        # events = events_result.get('items', [])
        #
        # if not events:
        #    print('No upcoming events found.')
        #    return


        # Prints the start and name of the next 10 events
        # for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()