import os
import csv
from fpdf import FPDF
from datetime import datetime, date
from django.shortcuts import render
from django.http import request, response

# CONSTANTS
WIDTH = 420
HEIGHT = 297

course_name = {
    'CS' : 'Computer Science and Engineering',
    'EE' : 'Electrical Engineering',
    'ME' : 'Mechanical Engineering'
}

grades = {'AA': 10, 'AB': 9, 'BB': 8, 'BC': 7, 'CC': 6, 'CD': 5, 'DD': 4, 'DD*': 4, 'F': 0, 'F*': 0, 'I': 0}

# FPDF CLASS
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 8)  # Arial bold 15

        self.rect(13, 13, WIDTH - 30, HEIGHT - 30) # page border
        self.line(13, 40, 403, 40) # horizontal line

        self.line(63, 13, 63, 40) # verical line
        self.line(353, 13, 353, 40) # verical line

        # IITP LOGO 
        self.image('static/iitp_logo2.jpg', 23, 15, 30, 20)
        self.image('static/iitp_logo2.jpg', 363, 15, 30, 20)

        self.set_xy(13, 37.5)
        self.cell(50, 0, 'INTERIM TRANSCRIPT', 0, 1, 'C')
        self.line(23, 39, 53, 39) # horizontal line for 'INTERIM TRANSCRIPT'

        self.set_xy(353, 37.5)
        self.cell(50, 0, 'INTERIM TRANSCRIPT', 0, 1, 'C')
        self.line(363, 39, 393, 39) # horizontal line for 'INTERIM TRANSCRIPT'
        
    def info_block(self, roll, name):
        self.rect(92, 42, 240, 13) # Inner Information Block

        self.set_font('Arial', 'B', 10)
        self.set_xy(92, 45)
        self.cell(21, 0, 'Roll No:', 0, 1, 'C')

        self.set_xy(115, 45)
        self.cell(20, 0, roll, 0, 1, 'C')

        self.set_xy(165, 45)
        self.cell(10, 0, 'Name:', 0, 1)

        self.set_xy(180, 45)
        self.cell(40, 0, name, 0, 1)

        self.set_xy(280, 45)
        self.cell(22, 0, 'Year of Admission:', 0, 1, 'C')

        self.set_xy(302, 45)
        self.cell(20, 0, f'20{roll[0 : 2]}', 0, 1, 'C')

        self.set_xy(165, 51)
        self.cell(10, 0, 'Course:', 0, 1)

        self.set_xy(180, 51)
        self.cell(50, 0, course_name[roll[4 : 6]], 0, 1)

        self.set_xy(92, 51)
        self.cell(28, 0, 'Programme:', 0, 1, 'C')

        self.set_xy(120, 51)
        self.cell(35, 0, 'Bachelor of Technology', 0, 1, 'C')

    def sem_num(self, sem_no, semX, semY):
        self.set_font('Arial', 'B', 9)
        self.set_xy(semX + 5.5, semY)
        self.cell(5, 0, f'Semester {sem_no}', 0, 1, 'C')
        self.line(semX, semY + 1.5, semX+ 16.5, semY + 1.5) # horizontal line

    def sem(self, semX, semY,  sem_no, l = ['Sub. Code', 'Subject Name', 'L-T-P', 'CRD', 'GRD']):
        #sem block
        self.rect(semX, semY, 122, 5)

        self.set_font('Arial', 'B', 7.5)
        self.line(semX + 15.5, semY, semX + 15.5, semY + 5) # sub code
        self.set_xy(semX, semY + 2.5)
        self.cell(15.5, 0, l[0], 0, 1, 'C')

        self.line(semX + 94.5, semY, semX + 94.5, semY + 5) # sub name
        self.set_xy(semX + 15.5, semY + 2.5)
        self.cell(79, 0, l[1], 0, 1, 'C')

        self.line(semX + 105.5, semY, semX + 105.5, semY + 5) # ltp
        self.set_xy(semX + 94.5, semY + 2.5)
        self.cell(11, 0, l[2], 0, 1, 'C')

        self.line(semX + 113.75, semY, semX + 113.75, semY + 5) # crd
        self.set_xy(semX + 105.5, semY + 2.5)
        self.cell(8.25, 0, l[3], 0, 1, 'C')

        self.set_xy(semX + 113.75, semY + 2.5) # grade
        self.cell(8.25, 0, l[4], 0, 1, 'C')

    def grade(self, semX, semY, credits, spi, cpi):
        # Grade Block
        self.rect(semX, semY + 2, 90, 6)

        self.set_xy(semX, semY + 5)
        self.cell(21, 0, 'Credits Taken:', 0, 1, 'C')

        self.set_xy(semX + 21, semY + 5)
        self.cell(7, 0, f'{credits}', 0, 1, 'C')

        self.set_xy(semX + 28, semY + 5)
        self.cell(22, 0, 'Credits Cleared:', 0, 1, 'C')

        self.set_xy(semX + 50, semY + 5)
        self.cell(7, 0, f'{credits}', 0, 1, 'C')

        self.set_xy(semX + 57, semY + 5)
        self.cell(10, 0, 'SPI:', 0, 1, 'C')

        self.set_xy(semX + 65, semY + 5)
        self.cell(7, 0, f'{spi}', 0, 1, 'C')

        self.set_xy(semX + 72, semY + 5)
        self.cell(10, 0, 'CPI:', 0, 1, 'C')

        self.set_xy(semX + 80, semY + 5)
        self.cell(7, 0, f'{cpi}', 0, 1, 'C')

    def signature(self, newY):
        # self.line(13, newY, 403, newY) # temp
        self.set_font('Arial', 'B', 10)

        self.set_xy(17.5, newY)
        self.cell(20, 0,'Date of Issue:', 0, 1)

        now = datetime.now()
        today = date.today()
        d2 = today.strftime("%d %B %Y")
        current_time = now.strftime("%H:%M")

        self.set_xy(45, newY)
        self.cell(45, 0, f'{d2}, {current_time}', 0, 1, 'C')

        self.line(45, newY + 3, 91, newY + 3) # horizontal line
        self.line(347, newY, 395, newY) # horizontal line

        self.set_xy(345, newY + 4)
        self.cell(46, 0, 'Assistant Registrar (Academic)', 0, 1)

def generateTranscript(type, list_of_roll = []):
    sub_info = {} # map of subject name & subject ltp 
    with open('sample_input/subjects_master.csv') as csvFile:
        f = csv.reader(csvFile)
        for row in f:
            if row[0] != 'subno':
                sub_info[row[0]] = []
                sub_info[row[0]].append(row[1])
                sub_info[row[0]].append(row[2])

    stud_master = {} # map of student name & subject rollno
    with open('sample_input/names-roll.csv') as csvFile:
        f = csv.reader(csvFile)
        for row in f:
            roll = row[0].upper()
            stud_master[roll] = row[1].upper()

    courses_cnt = {} # map for count of courses each sem
    with open('sample_input/grades.csv') as csvFile:
        f = csv.reader(csvFile)
        for row in f:
            if row[0] != 'Roll':
                roll = row[0].upper()
                sem_no = int(row[1])
                if roll not in courses_cnt:
                    courses_cnt[roll] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                courses_cnt[roll][sem_no - 1] += 1

    cnt = 0
    with open('sample_input/grades.csv') as csvFile:
        f = csv.reader(csvFile)
        for row in f:
            if row[0] != 'Roll':
                roll = row[0].upper()
                sem_no = int(row[1])

                if type == 1:
                    if roll not in list_of_roll:
                        continue
                if cnt == 0:
                    if sem_no == 1:
                        pos = [[17.5, 63], [145, 63], [272.5, 63]]
                        cnt = 0
                        pdf = PDF(orientation='L', unit='mm', format='A3')
                        pdf.add_page()
                        pdf.info_block(roll, stud_master[roll])
                        pdf.sem_num(1, pos[0][0], pos[0][1] - 3)
                        pdf.sem(pos[0][0], pos[0][1], 1)
                        cur_credits = 0
                        val = 0
                        credits = []
                        cpi = []
                        spi = []
                        pos[0][1] += 5
                    elif sem_no == 2 or sem_no == 5 or sem_no == 8:
                        cur_credits = 0
                        val = 0
                        pdf.sem_num(sem_no, pos[1][0], pos[1][1] - 3)
                        pdf.sem(pos[1][0], pos[1][1], sem_no)
                        pos[1][1] += 5
                    elif sem_no == 3 or sem_no == 6:
                        cur_credits = 0
                        val = 0
                        pdf.sem_num(sem_no, pos[2][0], pos[2][1] - 3)
                        pdf.sem(pos[2][0], pos[2][1], sem_no)
                        pos[2][1] += 5
                    elif sem_no == 4 or sem_no == 7:
                        cur_credits = 0
                        val = 0
                        curY = max(pos[0][1], pos[1][1], pos[2][1])
                        pdf.line(13, curY + 10, 403, curY + 10)
                        curY = curY + 10
                        pdf.sem_num(sem_no, pos[0][0], curY + 4)
                        pos[0][1] = curY + 7
                        pos[1][1] = curY + 7
                        pos[2][1] = curY + 7

                        pdf.sem(pos[0][0], pos[0][1], sem_no)
                        pos[0][1] += 5
                    
                if sem_no <= 8:
                    l = [row[2], sub_info[row[2]][0], sub_info[row[2]][1], row[3], row[4]]
                    pdf.sem(pos[(sem_no - 1) % 3][0], pos[(sem_no - 1) % 3][1], row[1], l)
                    pos[(sem_no - 1) % 3][1] += 5

                    # SPI Calculations
                    cur_credits += int(row[3])
                    val += int(row[3]) * grades[row[4].strip()]
                    cnt += 1

                    if cnt == courses_cnt[roll][sem_no - 1]:
                        credits.append(cur_credits)
                        spi.append(round(val / cur_credits, 2))

                        # CPI Calculations
                        sem_cpi = 0
                        prefix_credits = 0
                        for itr in range(0, len(spi)):
                            sem_cpi += spi[itr] * credits[itr]
                            prefix_credits += credits[itr]

                        pdf.grade(pos[(sem_no - 1) % 3][0], pos[(sem_no - 1) % 3][1], cur_credits, round(val / cur_credits, 2), round(sem_cpi / prefix_credits, 2))
                        if sem_no == 8:
                            curY = max(pos[0][0], pos[0][1])
                            curY += 10
                            newY = curY + (287 - curY) / 2
                            pdf.signature(newY)
                            pdf.output(f'transcriptsIITP/{roll}.pdf')

                            # removing the roll number from list_of_roll 
                            if type == 1:
                                list_of_roll.remove(roll)
                        cnt = 0

    return list_of_roll

# Create your views here.
def index(request):
    context = {}      
    if not os.path.exists('transcriptsIITP'):
        os.makedirs('transcriptsIITP')  
    return render(request, "index.html", context)

# generate range of transcripts
def range_transcript(request):
    roll_range = request.POST.get("roll_range")
    ls = roll_range.split('-')
    start = ls[0][6 : 8]
    end = ls[1][6 : 8]
    list_of_roll = []
    i = int(start)
    while i <= int(end):
        if i < 10:
            list_of_roll.append(f'{ls[0][0 : 6].upper()}0{i}')
        else:
            list_of_roll.append(f'{ls[0][0 : 6].upper()}{i}')
        i += 1

    try:
        remaining_roll = generateTranscript(1, list_of_roll)
    except:
        return response.HttpResponse('Some Error Occured')

    if len(remaining_roll) == 0:
        return response.HttpResponse('Successfully Generated transcripts')
    else:
        context = {
            'roll_no' : remaining_roll,
        }
        return render(request, 'result.html', context)

# generate all transcripts
def all_transcript(request):
    try:
        generateTranscript(2)
    except:
        return response.HttpResponse('Some Error Occured')
    return response.HttpResponse('Successfully Generated All Transcripts')