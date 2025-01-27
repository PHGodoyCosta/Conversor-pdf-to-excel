import os
import tabula
import PyPDF2

class ConvertingPDF:

    def __init__(self):
        self.csv = "result.csv"
        self.pdf = "Eurobet.pdf"
        self.mounth = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        self.columns = ["ORA", "MAN", "AVV", "DESCRIZIONE", "1X2", "Unnamed: 1", "DC"]
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
    
    def gettingPdfData(self, page):
        reader = tabula.read_pdf(self.pdf, pages=str(page), lattice=True)
        leitura = reader[1]
        df = leitura[self.columns]
        return df
    
    def organizingData(self, df):
        while self.counter <= 58:
            try:
                df["DISC"] = "1"
                df["NAZ"] = "0"
                df["CULT"] = "0"
                df["STATO"] = "A"
                df["PAL"] = "350"
                for h in self.columns:
                    if h == "ORA":
                        if len(str(df.loc[self.counter][h])) > 5:
                            s = str(df.loc[self.counter][h]).split(" ")
                            #print(s)
                            dia = self.addingZero(s[1])
                            for i in range(0, len(self.mounth)-1):
                                if s[2].lower() == self.mounth[i]:
                                    mes = self.addingZero(i + 1)
                            ano = s[3]
                            self.data = f"{dia}/{mes}/{ano}"
                            df = df.drop(self.counter, axis=0)
                        else:
                            #print(f"H: {df.loc[self.counter][h]}")
                            d = str(df.loc[self.counter][h]).replace(":", ".")
                            df.loc[self.counter, h] = f"{self.data} {d}"
                            df.loc[self.counter, "AVV"] = f"{str(int(float(str(df.loc[self.counter, 'AVV']))))}"
                        self.counter += 1
            except KeyError:
                self.error += 1
                if self.error > 40:
                    break
        self.counter = 0
        df = df.rename(columns={"AVV": "LINE", "MAN":"CAMPIONATO", "DESCRIZIONE":"EVENTO", "ORA":"DATA ORA", "1X2":"FN1", "Unnamed: 1":"FNX", "DC":"FN2"})
        return df[['DISC', 'PAL', 'LINE', 'CAMPIONATO', 'NAZ', 'CULT', 'EVENTO', 'DATA ORA', 'STATO', 'FN1', 'FNX', 'FN2']]

if __name__ == "__main__":
    starter = ConvertingPDF()
    archive = open(starter.pdf, "rb")
    reader = PyPDF2.PdfFileReader(archive)
    print("Processing...")
    for page in range(1, int(reader.numPages) + 1):
        df = starter.gettingPdfData(page)
        df = starter.organizingData(df)
        starter.addingToCsv(df)
    print("\nFinalized")

