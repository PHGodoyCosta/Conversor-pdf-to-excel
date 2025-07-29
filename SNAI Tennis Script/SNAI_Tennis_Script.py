import os
import tabula
import PyPDF2

class ConvertingPDF:

    def __init__(self):
        self.csv = "result.csv"
        if os.path.isfile(self.csv):
            os.unlink(self.csv)
        self.pdf = "snai.pdf"
        #self.pdf = "SNAITennis.pdf"
        self.mounth = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        self.columns = ["DIA", "Unnamed: 0", "Unnamed: 1", "Unnamed: 3", "Unnamed: 4", "Unnamed: 6", "Unnamed: 8", "Unnamed: 9"]
        self.reader_pdf = tabula.read_pdf(self.pdf, pages="all", lattice=True)
        self.counter = 0
        self.error = 0
        self.data = ""
        self.mes = ""
    
    def addingToCsv(self, df):
        if os.path.isfile(self.csv):
            df.to_csv(self.csv, index=False, sep=";", header=False, mode="a+")
        else:
            df.to_csv(self.csv, index=False, sep=";")

    def addingZero(self, data):
        if int(data) < 10:
            return f"0{data}"
        return str(data)
    
    def gettingYear(self, phrase):
        phrase = str(phrase)
        phrase = phrase.split("'")[1]
        phrase = phrase.split(",")[0]
        return f"20{phrase}"
    
    def gettingPdfData(self, page):
        reader = tabula.read_pdf(self.pdf, pages=str(page), lattice=True)
        leitura = reader[0]
        self.ano = self.gettingYear(list(leitura.columns)[0])
        leitura = leitura.rename(columns={list(leitura.columns)[0]: "DIA"})
        df = leitura[self.columns]
        self.limite = len(df)
        return df
    
    def organizingData(self, df):
        while self.counter <= self.limite + 4:
            try:
                df["DISC"] = "1"
                df["NAZ"] = "0"
                df["CULT"] = "0"
                df["STATO"] = "A"
                df["PAL"] = "350"
                df["FNX"] = "0"
                
                df.loc[self.counter]["DIA"] = f"{df.loc[self.counter]['DIA']}/{self.ano}"
                self.counter += 1
            except KeyError:
                self.error += 1
                if self.error > 40:
                    break
        self.counter = 0

        df = df.rename(columns={"Unnamed: 3": "LINE", "Unnamed: 8": "FN1", "Unnamed: 9": "FN2", "Unnamed: 1":"MAN"})
        df["EVENTO"] = df["Unnamed: 4"] + " - " + df["Unnamed: 6"]
        df["DATA ORA"] = df["DIA"] + " " + df["Unnamed: 0"]
        return df[['DISC', 'PAL', 'LINE', 'MAN', 'NAZ', 'CULT', 'EVENTO', 'DATA ORA', 'STATO', 'FN1', 'FNX', 'FN2']]
    
    def arrumandoArquivo(self):
        with open("result.csv", "r") as r:
            for text in r.readlines():
                found = text.find(";;")
                if found != -1:
                    text = text.replace("\n", "")
                    arquivo = open("result.csv", "r").read()
                    with open("result.csv", "w+") as f:
                        f.write(arquivo.replace(f"\n{text}", ""))
        arquivo = open("result.csv", "r").read()
        with open("result.csv", "w+") as f:
            found = arquivo.find("\n")
            text = arquivo[found + 1:]
            f.write(f"DISC;PAL;LINE;MAN;NAZ;CULT;EVENTO;DATA ORA;STATO;FN1;FNX;FN2\n{text}")

if __name__ == "__main__":
    starter = ConvertingPDF()
    archive = open(starter.pdf, "rb")
    reader = PyPDF2.PdfFileReader(archive)
    print("Processing...")
    for page in range(1, int(reader.numPages) + 1):
        df = starter.gettingPdfData(page)
        df = starter.organizingData(df)
        starter.addingToCsv(df)
    starter.arrumandoArquivo()
    print("\nFinalized")
