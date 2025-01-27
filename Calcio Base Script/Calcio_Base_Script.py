import os
import tabula
import PyPDF2

class ConvertingPdf:

    def __init__(self):
        self.csv = "result.csv"
        self.pdf = "calcio base per data.pdf"
        self.read_pdf = tabula.read_pdf(self.pdf, pages="all", lattice=True)
        self.colunas = ['Unnamed: 2', 'Unnamed: 0', 'Unnamed: 3', 'Unnamed: 4', 'CALCIO PER DATA', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']
        self.mounth = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
        self.dataCompleta = ""
        self.error = 0
        self.counter = 3

    def addingZero(self, data):
        if int(data) < 10:
            return f"0{data}"
        return str(data)
    
    def addingToCsv(self, df):
        if os.path.isfile(self.csv):
            df.to_csv(self.csv, index=False, sep=";", header=False, mode="a+")
        else:
            df.to_csv(self.csv, index=False, sep=";")
    
    def gettingDate(self, payload):
        payload = str(payload).split(" ")
        mounth = payload[2].replace(",", "").strip()
        for c in range(0, len(self.mounth)):
            if mounth == self.mounth[c]:
                mounth = self.addingZero(c + 1)
        return payload[1].strip(), mounth

    def gettingPdfData(self, page):
        read_pdf = tabula.read_pdf(self.pdf, pages=f"{page}", lattice=True)
        s = 0
        df = "Empty DataFrame"
        while str(df) == "Empty DataFrame":
            leitura = read_pdf[s]
            leitura = leitura[self.counter:]
            df = leitura[self.colunas]
            s += 1
        self.data = read_pdf[s].columns[0].replace("www.sisal.it | Quote soggette a variazioniDati aggiornati al ", "")
        self.ano = self.data.split("/")[2].split(" ")[0].strip()
        return df
    
    def gettingInformationDate(self, df):
        while self.counter <= 58:
            try:
                df["DISC"] = "1"
                df["NAZ"] = "0"
                df["CULT"] = "0"
                df["STATO"] = "A"
                df["PAL"] = "350"
                for h in self.colunas:
                    if h == "CALCIO PER DATA":
                        if len(df.loc[self.counter][h]) != 5:
                            day, mounth = self.gettingDate(df.loc[self.counter][h])
                            self.dataCompleta = f"{day}/{mounth}/{self.ano}"
                            df = df.drop(self.counter, axis=0)
                        else:
                            df.loc[self.counter][h] = f"{self.dataCompleta} {df.loc[self.counter][h]}"
                        self.counter += 1
            except KeyError:
                self.error += 1
                if self.error > 40:
                    break
        self.counter = 3
        df = df.rename(columns={"Unnamed: 2": "LINE", "Unnamed: 0":"CAMPIONATO", "Unnamed: 3":"EVENTO", "Unnamed: 4": "EVENTO2", "CALCIO PER DATA":"DATA ORA", "Unnamed: 6":"FN1", "Unnamed: 7":"FNX", "Unnamed: 8":"FN2"})
        df["EVENTO"] = df["EVENTO"] + " - " + df["EVENTO2"]
        return df[['DISC', 'PAL', 'LINE', 'CAMPIONATO', 'NAZ', 'CULT', 'EVENTO', 'DATA ORA', 'STATO', 'FN1', 'FNX', 'FN2']]

if __name__ == "__main__":
    starter = ConvertingPdf()
    file = open(starter.pdf, "rb")
    reader = PyPDF2.PdfFileReader(file)
    print("\nProcessing...")
    for page in range(1, int(reader.numPages) + 1):
        df = starter.gettingPdfData(page)
        df = starter.gettingInformationDate(df)
        starter.addingToCsv(df)
    print("Finished!")
