import os
from fpdf import FPDF

WIDTH = 420
HEIGHT = 297

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 8)  # Arial bold 15
        # self.ln(26)
        
    def lines(self):
        self.rect(13, 13, WIDTH - 30, HEIGHT - 30) # page border
        self.line(13, 40, 403, 40) # horizontal line

        self.line(63, 13, 63, 40) # verical line
        self.line(353, 13, 353, 40) # verical line

        self.line(23, 39, 53, 39) # horizontal line for 'INTERIM TRANSCRIPT'
        self.line(363, 39, 393, 39) # horizontal line for 'INTERIM TRANSCRIPT'

        self.rect(92, 42, 240, 13) # Inner Information Block


pdf = PDF(orientation='L', unit='mm', format='A3')
pdf.add_page()

# IITP LOGO 
pdf.image('static/iitp_logo2.jpg', 23, 15, 30, 20)
pdf.image('static/iitp_logo2.jpg', 363, 15, 30, 20)

pdf.set_xy(13, 37.5)
pdf.cell(50, 0, 'INTERIM TRANSCRIPT', 0, 1, 'C')

pdf.set_xy(353, 37.5)
pdf.cell(50, 0, 'INTERIM TRANSCRIPT', 0, 1, 'C')

# Inner Information Block
pdf.set_font('Arial', 'B', 10)
pdf.set_xy(92, 45)
pdf.cell(21, 0, 'Roll No:', 0, 1, 'C')

pdf.set_xy(92, 51)
pdf.cell(28, 0, 'Programme:', 0, 1, 'C')

pdf.set_xy(160, 45)
pdf.cell(22, 0, 'Name:', 0, 1, 'C')

pdf.set_xy(160, 51)
pdf.cell(24, 0, 'Course:', 0, 1, 'C')

pdf.set_xy(280, 45)
pdf.cell(22, 0, 'Year of Admission:', 0, 1, 'C')

# Semester 
pdf.set_xy(15, 56)
pdf.cell(10, 0, 'Semester 1', 0, 1, 'C')

print(pdf.get_x(), pdf.get_y())

pdf.lines()

pdf.output('test.pdf')
