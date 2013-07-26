# coding=utf-8

import urllib2
import lxml.html
	

# Classe para a captura da lista de projetos
class projetos:
	def __init__(self):	
		self.arquivos = []
			
	def capturaPagina(self, pagina='1', sigla='', numero='', ano='', autor=''):

		response = urllib2.urlopen('http://www.camara.gov.br/sileg/Prop_lista.asp?Pagina=%s&sigla=%s&Numero=%s&Ano=%s&Autor=%s&OrgaoOrigem=todos&Comissao=0&Situacao=&dtInicio=&dtFim=&Ass1=&co1=+AND+&Ass2=&co2=+AND+&Ass3=&Submit=Pesquisar&Relator=&pesqCompleta=1' %(pagina, sigla, numero, ano, autor))
		
   		html = response.read()
		   		
		arvore = lxml.html.fromstring(html)

		elementos = arvore.find_class("rightIconified iconDetalhe")
		
		for elemento in elementos:
			tags = elemento.values()
			tag = tags[0]
			tag = tag.split('=')
			indice = tag[1]
			self.arquivos.append(indice)
		
		
   		
   		
	def captura(self, sigla='', numero='', ano='', autor=''):
		indice = 0
		while (True):
			comeco = len(self.arquivos)
			try: self.capturaPagina(indice, sigla, numero, ano, autor)
			except: break
			indice+=1
			if(comeco == len(self.arquivos)):
				break
			


# Classe para a captura de detalhes
class detalhes:
	def __init__(self):	
		self.nome = ''		
		self.indice = ''	
		self.tipo = ''		
		self.autor = ''		
		self.completo = ''	
		self.ementa = ''	
		self.tags = []		
		self.tramitacoes = []
		self.html = ''
		self.apresentacao = ''
		self.situacao = ''
			
	def captura(self, indice):
		
		response = urllib2.urlopen('http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=%s' % indice)
	
   		html = response.read()   		
		   		
		arvore = lxml.html.fromstring(html)
		
		# HTML
		self.html = html
		
		# indice
		self.indice = indice
		
		# projeto completo
		self.completo = 'http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor='+indice

		# nome
		elementos = arvore.find_class('nomeProposicao')
		elemento = elementos[0]
		self.nome = elemento.text
		
		# tipo
		elementos = arvore.find_class('tipoProposicao')
		elemento = elementos[0]
		self.tipo = elemento.text
		
		# autor
		elementos = arvore.get_element_by_id('colunaPrimeiroAutor')
		elementos = elementos.getchildren()
		elemento = elementos[2]
		self.autor = elemento.text.strip()
		
		# tags de busca
		try:
			elementos = arvore.get_element_by_id('textoIndexacao')
			self.tags = elementos.text.split(', ')
		except:
			self.tags =[]
			
		#ementa
		elementos = arvore.find_class('textoJustificado')
		elemento = elementos[0]
		self.ementa = elemento.text
		
		# situaçao 
		elementos = arvore.get_element_by_id('subSecaoSituacaoOrigemAcessoria')
		elemento = elementos.getchildren()
		elemento = elemento[0].getchildren()[1]
		
		self.situacao = elemento.text.strip()
		
		
		# tramitaçoes
		elementos = arvore.get_element_by_id('tramitacoes')
		
		datas = []
		for data in elementos.cssselect('td'):
			if (data.text.strip() != ''):
				datas.append(data.text.strip())
				
		# apresentacao
		self.apresentacao = datas[0]
		
		orgaos = []
		for orgao in elementos.cssselect('strong'):
			orgaos.append(" ".join(orgao.text.split()))
			
		fatos = []
		for fato in elementos.cssselect('li'):
			fatos.append(fato.text.strip())
			
		while datas != []:
			tramit = []
			tramit.append(datas.pop())
			tramit.append(orgaos.pop())
			tramit.append(fatos.pop())
			self.tramitacoes.append(tramit)

			
	def interpreta(self, indice):
	  	if (self.html == '')	:
			return False
		
		arvore = lxml.html.fromstring(self.html)
		
		# indice
		self.indice = indice
		
		# projeto completo
		self.completo = 'http://www.camara.gov.br/proposicoesWeb/prop_mostrarintegra?codteor='+indice

		# nome
		elementos = arvore.find_class('nomeProposicao')
		elemento = elementos[0]
		self.nome = elemento.text
		
		# tipo
		elementos = arvore.find_class('tipoProposicao')
		elemento = elementos[0]
		self.tipo = elemento.text
		
		# autor
		elementos = arvore.get_element_by_id('colunaPrimeiroAutor')
		elementos = elementos.getchildren()
		elemento = elementos[2]
		self.autor = elemento.text.strip()
		
		# tags de busca
		try:
			elementos = arvore.get_element_by_id('textoIndexacao')
			self.tags = elementos.text.split(', ')
		except:
			self.tags =[]
			
		#ementa
		elementos = arvore.find_class('textoJustificado')
		elemento = elementos[0]
		self.ementa = elemento.text
		
		# situaçao 
		elementos = arvore.get_element_by_id('subSecaoSituacaoOrigemAcessoria')
		elemento = elementos.getchildren()
		elemento = elemento[0].getchildren()[1]
		
		self.situacao = elemento.text.strip()
		
		
		# tramitaçoes
		elementos = arvore.get_element_by_id('tramitacoes')
		
		datas = []
		for data in elementos.cssselect('td'):
			if (data.text.strip() != ''):
				datas.append(data.text.strip())
				
		# apresentacao
		self.apresentacao = datas[0]
		
		orgaos = []
		for orgao in elementos.cssselect('strong'):
			orgaos.append(" ".join(orgao.text.split()))
			
		fatos = []
		for fato in elementos.cssselect('li'):
			fatos.append(fato.text.strip())
			
		while datas != []:
			tramit = []
			tramit.append(datas.pop())
			tramit.append(orgaos.pop())
			tramit.append(fatos.pop())
			self.tramitacoes.append(tramit)

			
	def lista(self, dado=''):
		if (dado == ''):
			return [self.nome, self.indice, self.tipo ,self.autor,self.completo,self.ementa,self.tags ,self.tramitacoes]
		

		
		
		


