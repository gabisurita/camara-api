# usr/lib python3.3
# coding=utf-8

import os
import sys
import camaraAPI
import urllib2
import codecs
import sqlite3

siglas = ['PL', 'PLP', 'MPV', 'PEC', 'PDC', 'PRC', 'ADD', 'APJ', 'ATC', 'TVR', 'ATOP', 'AA', 'AV', 'AVN', 'CVO', 'CAC', 'CON', 'CCN', 'CVR', 'CST', 'DEC', 'DVT', 'DEN', 'DCR', 'DTQ', 'DOC', 'EMD', 'EML', 'EMA', 'EMO', 'EPP', 'ESB', 'EMP', 'ERD', 'EMR', 'EMRP', 'EMC', 'EAG', 'ESP', 'EMS', 'ERR', 'EXP', 'IAN', 'INC', 'INA', 'MAN', 'MSC', 'MCN', 'MSG', 'MSF', 'RTV', 'MMP', 'MST', 'MTC', 'NINF', 'NIC', 'OBJ', 'OF', 'STF', 'OFN', 'SGM', 'OFS', 'OF.', 'OFT', 'P.C', 'PEA', 'PRST', 'PES', 'PEP', 'PSS', 'PSS', 'PAR', 'PARF', 'PRL', 'PRP', 'PPP', 'PPP', 'PRR', 'PPR', 'PRT', 'PRV', 'PCA', 'PDA', 'PET', 'PRA', 'PDN', 'PDS', 'PLN', 'PLC', 'PLV', 'PLS', 'PLOA', 'PRN', 'PRF', 'PRO', 'PFC', 'PRVP', 'RCM', 'REM', 'REC', 'R.C', 'RDV', 'RDF', 'RST', 'RFP', 'REL', 'CAE', 'CAE', 'RRC', 'RRC', 'COI', 'RRL', 'RLF', 'RPA', 'RPL', 'RPL', 'RPLE', 'RLP', 'RLP(R)', 'RLP(V)', 'RAT', 'REP', 'RPR', 'REQ', 'RIC', 'RCP', 'RQP', 'RIN', 'RQN', 'RQA', 'RQC', 'SIT', 'SBE', 'SAP', 'SSP', 'SBT', 'SUG', 'SUC', 'SDL', 'SLD', 'SRL', 'SOA', 'SOR', 'SPA', 'SPP', 'SPA-R', 'SPP-R', 'SRAP', 'SUM', 'TER', 'VTS']

anos = [2013, 1988]

def menu():
	ajuda = 'Uso: Captura [-c (só captura)][-i (só interpreta)][-a "ano"][-t "tipo"]'
	
	if len(sys.argv) < 2:
		auto()

	elif "-h" in sys.argv:
		print(ajuda)

	elif "-c" in sys.argv:
		if "-i" in sys.argv:
			auto()
		else:
			captura()
	
	elif "-i" in sys.argv:
		interpreta()


	elif "-a" in sys.argv:	
		ano = sys.argv[sys.argv.index("-a") + 1]
		anos = [int(ano),int(ano) -1]
		auto()
	
	elif "-t" in sys.argv:	
		tipo = sys.argv[sys.argv.index("-t") + 1]
		siglas = [tipo]
		auto()
	
	else:
		print(ajuda)
	


def auto():

	con1 = sqlite3.connect('Camara.sqlite')
	c1 = con1.cursor()
	con2 = sqlite3.connect('RAWCamara.sqlite')
	c2 = con2.cursor()
	

	c1.execute('CREATE TABLE IF NOT EXISTS projetos (indice INTEGER PRIMARY KEY, nome TEXT, tipo TEXT, autor TEXT,apresentacao TEXT,situacao TEXT, completo TEXT, ementa TEXT,tags TEXT)')


	c2.execute('CREATE TABLE IF NOT EXISTS html(indice INTEGER, html TEXT)')

	con1.commit()
	con2.commit()


	for ano in range(anos[0],anos[1],-1):
		for sigla in siglas:
			ano = str(ano)
			numero = ''
			autor = ''
			pagina = ''
	
			Projetos = camaraAPI.projetos()
			print(u'Juntando informações sobre o ano de ' + ano + ' tipo ' + sigla)
			Projetos.captura(sigla, numero, ano, autor)

	
			semDuplicatas = []
			for x in Projetos.arquivos:
				if x not in semDuplicatas:
					semDuplicatas.append(x)

			con2.commit()

			print(u'Começando captura de dados')
			for arquivo in semDuplicatas:
				infos = camaraAPI.detalhes()
				try:
					infos.captura(arquivo)
							
					c2.execute('INSERT OR REPLACE INTO html (indice, html) VALUES (?,?)', (infos.indice, buffer(infos.html)))

					c1.execute('INSERT OR REPLACE INTO projetos (indice, nome, tipo, autor,apresentacao,situacao, completo, ementa, tags) VALUES (?,?,?,?,?,?,?,?,?)', (infos.indice, infos.nome, infos.tipo, infos.autor, infos.apresentacao, infos.situacao, infos.completo, infos.ementa, u":".join(infos.tags)))

				
					print(infos.nome)

				except:
					print('Con falhou!')

				con1.commit()
				con2.commit()

	con1.close()	
	con2.close()	

	
def captura():	
	con2 = sqlite3.connect('RAWCamara.sqlite')
	c2 = con2.cursor()
	



	c2.execute('CREATE TABLE IF NOT EXISTS html(indice INTEGER, html TEXT)')

	con2.commit()


	for ano in range(anos[0],anos[1],-1):
		for sigla in siglas:
			ano = str(ano)
			numero = ''
			autor = ''
			pagina = ''
	
			Projetos = camaraAPI.projetos()
			print(u'Juntando informações sobre o ano de ' + ano + ' tipo ' + sigla)
			Projetos.captura(sigla, numero, ano, autor)

	
			semDuplicatas = []
			for x in Projetos.arquivos:
				if x not in semDuplicatas:
					semDuplicatas.append(x)

			con2.commit()

			print(u'Começando captura de dados')
			for arquivo in semDuplicatas:
				infos = camaraAPI.detalhes()
				try:
					infos.captura(arquivo)
							
					c2.execute('INSERT OR REPLACE INTO html (indice, html) VALUES (?,?)', (infos.indice, buffer(infos.html)))

				
					print(infos.nome)

				except:
					print('Con falhou!')

				con2.commit()

	con2.close()	
	
def interpreta():

	con1 = sqlite3.connect('Camara.sqlite')
	c1 = con1.cursor()
	con2 = sqlite3.connect('RAWCamara.sqlite')
	c2 = con2.cursor()
	

	c1.execute('CREATE TABLE IF NOT EXISTS projetos (indice INTEGER PRIMARY KEY, nome TEXT, tipo TEXT, autor TEXT,apresentacao TEXT,situacao TEXT, completo TEXT, ementa TEXT,tags TEXT)')


	con1.commit()

	arquivos = c2.execute("select * from html")


	for arq in arquivos:
		#try:
			arquivo = arquivos.fetchone()
			
			infos = camaraAPI.detalhes()
			
			infos.indice = str(arquivo[0])
			infos.html = str(arquivo[1])
			
			infos.interpreta(str(arquivo[0]))
			
			c1.execute('INSERT OR REPLACE INTO projetos (indice, nome, tipo, autor,apresentacao,situacao, completo, ementa, tags) VALUES (?,?,?,?,?,?,?,?,?)', (infos.indice, infos.nome, infos.tipo, infos.autor, infos.apresentacao, infos.situacao, infos.completo, infos.ementa, u":".join(infos.tags)))

		
			print(infos.nome)

		#except:
		#	print('Con falhou!')

			con1.commit()
			con2.commit()

	con1.close()	
	con2.close()	

if __name__ == "__main__":
	menu()
