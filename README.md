                                              SimplyCalendar - SparkHack 2023 UIC

Team Members:
Gor,
Kenneth,
Ahmad,
Vincenzo

Project Description: <br />
SimplyCalendar is a Python application designed to help users easily import their class schedules from an HTML file and export class information. 
This includes the class name, day, and time and automatically exports it to the student's Google Calendar. 
While thinking of a project idea, we wanted to address our immediate community, our fellow students.
We decided to build this project to simplify the process of adding class schedules to calendar applications and save time for students by minimizing the complexity of exporting class schedules into Calendar.

Key Features: <br />
Automatically parses class information from HTML file
Extracts relevant class details, such as class name, day, and time
Exports class information in a format compatible with Google Calendar automatically
Streamlines the process of adding classes to a calendar

Implementation Details: <br />
SimplyCalendar is built using Python for parsing HTML files. 
The program takes an HTML file as input, processes the file using the Google Calendar API to extract the required class information
It exports the class details automatically to the user’s Google account/email

Usage Instructions: <br />
Login on my.uic.edu -> XE Registration -> Register for classes -> Semester you want saved (e.g. Fall 23)
After the class schedule page loads, press the following keys: cmd + s and save your html file to a folder that contains the SimplyCalendar program
Run the program with your HTML file in the same directory
The program will output class information in a format compatible with Google Calendar

Future Improvements: <br />
Support for additional calendar applications
Automatic integration with calendar APIs for seamless import
Enhanced error handling and input validation
Support for extracting additional class information, such as location and instructor
Support images in addition to html file to export class information

Conclusion: <br />
SimplyCalendar aims to make the process of adding class schedules to calendars effortlessly. 
By automating the extraction and export of class information from an HTML file, UIC students can save time and seamlessly add their class schedules to Google Calendar. 
This streamlines the process and offers accessibility to users that may be confused with exporting their school schedule with the current implementation
