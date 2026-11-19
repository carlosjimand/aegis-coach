import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

pdf_path = .agents/spec_miner_markitdown/test_sample.pdf
c = canvas.Canvas(pdf_path, pagesize=letter)
c.drawString(100, 750, Test Scientific Paper Title)
c.drawString(100, 700, Abstract: This is a sample paper testing markitdown extraction.)
c.drawString(100, 650, Section 1: Polarized Training (80/20))
c.drawString(100, 600, Askling L-Protocol for Hamstring rehabilitation.)
c.save()
print(fPDF generated successfully at {pdf_path})
