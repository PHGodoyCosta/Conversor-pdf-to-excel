<div align=center>
    <img src="images/poster.png">
</div>

# Conversor de PDF em Excel

> Um Freelance que fiz para plataforma para um Italiano que precisava converter uma tabela em **PDF** de resultado de jogos em **.csv**

![Python](https://img.shields.io/badge/Python-3.10+-356e9f?style=for-the-badge&logo=python&logoColor=white)![Pandas](https://img.shields.io/badge/Pandas-2.0.3+-19227a?style=for-the-badge&logo=pandas&logoColor=white) 

### Matéria completa:

Se quiser sobre toda a história de desenvolvimento, como foi minha primeira experiência com a plataforma [freelacer.com](https://freelacer.com/) e o contexto desse projeto, leia a matéria que escrevi no meu [Site Portfólio](https://phgodoycosta.com.br/)

**Link da Matéria Completa:** [https://phgodoycosta.com.br/projeto/conversor-pdf-to-excel](https://phgodoycosta.com.br/projeto/conversor-pdf-to-excel)

Esse foi um dos trabalhos freelances que fiz para um rapaz italiano no freelance.com em 2022.

Ele tinha alguns PDF de resultados esportivos, e precisava de um script em python que conseguisse ler as tabelas com os resultados, e exportar em um arquivo .csv no formato em que ele pedia.

Para isso, usei a biblioteca [Tabula](https://tabula-py.readthedocs.io/en/latest/), um dos requirimentos para ela funcionar, é ter o Java instalado.

Mas basicamente o que ela faz é transformar a tabela que ela encontrar dentro do PDF em um Dataframe do [Pandas](https://pandas.pydata.org/).

Depois, todo o trabalho está com o Pandas. O problema é que todos os Dataframes, viam "quebrados". Dados de uma coluna jogados para outra, informações que eu não precisava...

Mas por sorte eles tinham um padrão nesses defeitos, então usei o Jupyter Notebook para analisar e arrumar tudo com o script.

## 📦 Instalação

```bash
# Clonar o repositório
$ https://github.com/PHGodoyCosta/Conversor-pdf-to-excel
$ cd Conversor-pdf-to-excel

# Instalando dependências
$ pip3 install -r requirements.txt

#OBS... Cada pasta é referente a um script e um trabalho diferente, para executar cada um pasta:

$ cd "<Pasta Especifica>"

# Inicie programa com:
$ python3 "<Nome do arquivo>.py"
```