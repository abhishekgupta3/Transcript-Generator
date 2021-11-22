import os
from fpdf import FPDF

WIDTH = 420
HEIGHT = 297

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)  # Arial bold 15

    def lines(self):
        self.rect(10, 10, WIDTH - 20, HEIGHT - 20)
        self.line(10, 38, 410, 38)


pdf = PDF(orientation='L', unit='mm', format='A3')
pdf.add_page()
pdf.lines()
pdf.output('test.pdf')
