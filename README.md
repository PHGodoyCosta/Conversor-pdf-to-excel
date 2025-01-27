# Conversor de PDF em Excel

Esse foi um dos trabalhos freelances que fiz para um rapaz italiano no freelance.com em 2022.

Ele tinha alguns PDF de resultados esportivos, e precisava de um script em python que conseguisse ler as tabelas com os resultados, e exportar em um arquivo .csv no formato em que ele pedia.

Para isso, usei a biblioteca [Tabula](https://tabula-py.readthedocs.io/en/latest/), um dos requirimentos para ela funcionar, é ter o Java instalado.

Mas basicamente o que ela faz é transformar a tabela que ela encontrar dentro do PDF em um Dataframe do [Pandas](https://pandas.pydata.org/).

Depois, todo o trabalho está com o Pandas. O problema é que todos os Dataframes, viam "quebrados". Dados de uma coluna jogados para outra, informações que eu não precisava...

Mas por sorte eles tinham um padrão nesses defeitos, então usei o Jupyter Notebook para analisar e arrumar tudo com o script.