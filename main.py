
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fpdf import FPDF
from urllib.parse import unquote

app = FastAPI()

class AlefimPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(102, 0, 204)
        self.cell(0, 10, "Alefim - Sua História Mágica", ln=True, align="C")

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_final_pages(self):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "Desenhe aqui o que você mais gostou da história!", ln=True)
        self.ln(20)
        self.rect(20, 40, 170, 120)

        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "Qual será a próxima aventura?", ln=True)
        self.ln(20)
        self.rect(20, 40, 170, 120)

def generate_pdf(heroi: str, historia: str, tipo: str):
    pdf = AlefimPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    partes = historia.split("\n\n")
    for par in partes:
        pdf.chapter_body(par.strip())

    pdf.add_final_pages()

    filename = f"{tipo}_{heroi.replace(' ', '_')}.pdf"
    filepath = f"/tmp/{filename}"  # <<< corrigido aqui
    pdf.output(filepath)
    return filepath

@app.get("/api/pdf-curto")
def gerar_pdf_curto(heroi: str, ajudante: str, poder: str, lugar: str, historia: str):
    historia_decodificada = unquote(historia)
    return FileResponse(generate_pdf(heroi, historia_decodificada, "curto"), filename=f"historia_curta_{heroi}.pdf")

@app.get("/api/pdf-longo")
def gerar_pdf_longo(heroi: str, ajudante: str, poder: str, lugar: str, desafio: str, mensagem: str, presente: str, historia: str):
    historia_decodificada = unquote(historia)
    return FileResponse(generate_pdf(heroi, historia_decodificada, "longo"), filename=f"historia_longa_{heroi}.pdf")
