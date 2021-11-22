import os
from fpdf import FPDF

WIDTH = 420
HEIGHT = 297

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)  # Arial bold 15

    def lines(self):
        self.rect(10, 10, WIDTH - 20, HEIGHT - 20) # page border
        self.line(10, 38, 410, 38) # horizontal line
        self.line(60, 10, 60, 38) # verical line
        self.line(360, 10, 360, 38) # verical line


pdf = PDF(orientation='L', unit='mm', format='A3')
pdf.add_page()
pdf.image('static/iitp_logo.png', 20, 13, 30, 20)
pdf.image('static/iitp_logo.png', 370, 13, 30, 20)
pdf.lines()
pdf.output('test.pdf')
