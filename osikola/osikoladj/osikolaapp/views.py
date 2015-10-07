from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.db import connection
from django.template import Template, Context, RequestContext
from .models import Cacesso
from .forms import Home,EditarDadosAcesso
from datetime import date
import datetime
from django.core.urlresolvers import reverse

# Create your views here.
def dictfetchall(cursor):
	desc = cursor.description
	return [dict(zip([call[0] for call in desc],raw)) for raw in cursor.fetchall()]


def carregarEscola():
	escola = connection.cursor()
	escola.execute("select * from tblEscolaActual");
	return dictfetchall(escola)

def ActualizarUtilizadores(utilizador,password,CodFuncionario):
        login = connection.cursor()
        login.execute("update tblContasDeAcesso set Utilizador='%s', Senha= '%s' where CodFuncionario ='%d'" %(utilizador,password,CodFuncionario));
        return login

def confirmarLoginFuncionario(user,password,ano):
	login = connection.cursor()
	login.execute("select * from tblContasDeAcesso where Utilizador='%s' and Senha= '%s' and AnoLectivo='%s'" %(user,password,ano));
	return dictfetchall(login)

#______________________FUNCIONARIOS_______________________
def carregarFuncionarios(CodFuncionario):
	funcionario = connection.cursor()
	funcionario.execute("select tblIdentificacao.Numero,tblFuncionario.Nome,tblFuncionario.NumeroCIF from tblIdentificacao WITH (NOLOCK) JOIN tblFuncionario On tblFuncionario.IdIdentificacao = tblIdentificacao.CodIdentificacao where tblFuncionario.CodFuncionario= '%s' ORDER BY Nome" %(CodFuncionario));
	return dictfetchall(funcionario)


def carregarPais():
        query = connection.cursor()
        query.execute("select * from tblPai WITH (NOLOCK)");
        return dictfetchall(query)


def carregarProvincia(valor):
        query = connection.cursor()
        query.execute("select *from tblProvincia Where CodPais =  '%s'" %valor);
        return dictfetchall(query)

def carregarMunicipio(valor):
        query = connection.cursor()
        query.execute("select * from tblMunicipio Where CodProvincia = '%s'" %valor);
        return dictfetchall(query)


#____________________________________________
def show_image(request):
	escola=carregarEscola()
	logotipo = escola[0]['Logotipo']
	binaryStuff = logotipo.asString('png')
	return HttpResponse(binaryStuff, 'image/png')

def get_editar_funcionario(valor):
	query = connection.cursor()
	query.execute("select * from tblFuncionario where CodFuncionario='%s' " %valor);
	return dictfetchall(query)

def editarDadosAcesso(request):
        template = 'editarContaDeAcesso.html'
        if request.session['user']:
                valor = request.session['id_user']
                form = EditarDadosAcesso(request.POST)
                if form.is_valid():
                        Senha= form.cleaned_data['password']
                        Senha2= form.cleaned_data['ConfirmarPassword']

                        Utilizador = form.cleaned_data['utilizador']
                        if Senha == Senha2:
                                ActualizarUtilizadores(Utilizador,Senha,valor)
                        else:
                                resultado='As palavras passes nao combinam. Preencha novamente'

                                return render(request,template,{'resultado':resultado})

                        return HttpResponseRedirect('/professores/')
        professor=carregarFuncionarios(request.session['id_user'])
        escola=carregarEscola()
        return render(request,template)

def iniciop(request):
	template = 'iniciop.html'
	professor=carregarFuncionarios(request.session['id_user'])
	escola=carregarEscola()
	return render(request,template,{'professor':professor,'escola':escola,'graph':reverse('show_image')})
	
def EditarDadosPessoais(request):
	try:
		if request.session['user']:
        		valor = request.session['id_user']
        		resultado = get_editar_funcionario(valor)
        		#print 'Resultado--------------', resultado	

        		if request.method == 'POST':
                		form = MembroForm(request.POST, request.FILES)
                		if form.is_valid():
                        		resultado = get_editar_funcionario(valor)
                        		resultado.Nome = forms.cleaned_data['Nome']
                        		resultado.Pseodonimo = forms.cleaned_data['Pseodonimo']
                        		resultado.Sexo = forms.cleaned_data['Sexo']
                        		resultado.DataNascimento = forms.cleaned_data['DataNascimento']
                        		resultado.Idade = forms.cleaned_data['Idade']
                        		resultado.CodComuna = forms.cleaned_data['CodComuna']
                        		resultado.CodPai = forms.cleaned_data['CodPai']
                        		resultado.CodMae = forms.cleaned_data['CodMae']
                        		resultado.IdIdentificacao = forms.cleaned_data['IdIdentificacao']
                        		resultado.CodEstadoCivil = forms.cleaned_data['CodEstadoCivil']
                        		resultado.NomeConjuge = forms.cleaned_data['NomeConjuge']
                        		resultado.Residencia = form.cleaned_data['Residencia']   
                        		resultado.Numerocasa = form.cleaned_data['Numerocasa']
                        		resultado.Telefone = form.cleaned_data['Telefone']
                        		resultado.NumerodeConta = form.cleaned_data['NumerodeConta']
                        		resultado.IDEntidadeBancaria = form.cleaned_data['IDEntidadeBancaria']
                        		resultado.NumeroFilhos = form.cleaned_data['NumeroFilhos']
                        		resultado.CodGrupoSanguineo = form.cleaned_data['CodGrupoSanguineo']
                        		resultado.CodProfissao = form.cleaned_data['CodProfissao']
                        		resultado.CodCarreira = form.cleaned_data['CodCarreira']
                        		resultado.CodCategoria = form.cleaned_data['CodCategoria']
                        		resultado.DataInicioCategoria = form.cleaned_data['DataInicioCategoria']
                        		resultado.NumeroAgente = form.cleaned_data['NumeroAgente']
                        		resultado.NumeroCIF = form.cleaned_data['NumeroCIF']
                        		resultado.SalarioBase = form.cleaned_data['SalarioBase']
                        		resultado.DataIngressoFuncaoPublica = form.cleaned_data['DataIngressoFuncaoPublica']
                        		resultado.DataInicioFuncaoPublica = form.cleaned_data['DataInicioFuncaoPublica']
                        		resultado.DataInicioFuncaoNaEscola = form.cleaned_data['DataInicioFuncaoNaEscola']
                        		resultado.CodFuncao = form.cleaned_data['CodFuncao']
                        		resultado.DataNomeacao = form.cleaned_data['DataNomeacao']
                        		resultado.NumeroDRN = form.cleaned_data['NumeroDRN']
                        		resultado.Serie=form.cleaned_data['Serie']
                        		resultado.Transferido=form.cleaned_data['Transferido']
                        		resultado.CodLocalServicoAnterior=form.cleaned_data['CodLocalServicoAnterior']
                        		resultado.DataTransferencia=form.cleaned_data['DataTransferencia']
                        		resultado.PorOrdemde=form.cleaned_data['PorOrdemde']
                        		resultado.OutrosLocais=form.cleaned_data['OutrosLocais']
                        		resultado.ServicoMilitar=form.cleaned_data['ServicoMilitar']
                        		resultado.DataIncorporacao=form.cleaned_data['DataIncorporacao']
                        		resultado.DataDesmobilizacao=form.cleaned_data['DataDesmobilizacao']
                        		resultado.NumeroDocumento=form.cleaned_data['NumeroDocumento']
                        		resultado.Codtalao=form.cleaned_data['Codtalao']
                        		resultado.CodHabilitacoesliterareas=form.cleaned_data['CodHabilitacoesliterareas']
                        		resultado.CodAnoConclusao=form.cleaned_data['CodAnoConclusao']
                        		resultado.CodInstituicao=form.cleaned_data['CodInstituicao']
                        		resultado.CodEspecialidade=form.cleaned_data['CodEspecialidade']
                        		resultado.CodHabilitacoesProfissionais=form.cleaned_data['CodHabilitacoesProfissionais']
                        		resultado.CodAnoConclusao2=form.cleaned_data['CodAnoConclusao2']
                        		resultado.CodInstituicao2=form.cleaned_data['CodInstituicao2']
                        		resultado.ExperienciaPratica=form.cleaned_data['ExperienciaPratica']
                        		resultado.Observacoes=form.cleaned_data['Observacoes']
                                        resultado.DataInsercao=form.cleaned_data['DataInsercao']
                        		resultado.Fotografia=forms.ImageField(label='Seleccionar imagem', required=False)

                        		#resultado.provincia = Provincia.objects.get(nomeDaProvincia=form.cleaned_data['provincia'])
                        		
                        		resultado.foto=request.FILES['foto']
                        		resultado.save()
                        		return HttpResponseRedirect('/gestao/membro/pesquisar/')
				
	except:
		return HttpResponseRedirect('/')
	template = 'EditarDadosPessoais.html'
	professor=carregarFuncionarios(request.session['id_user'])
	escola=carregarEscola()
	return render(request,template,{'resultado':resultado,'professor':professor,'escola':escola,'graph':reverse('show_image')})


def loginProfessores(request):
	ano= datetime.date.today().year
	template = 'loginProfessores.html'
        if request.method == 'GET':
        	user = request.GET.get('email')
	        password = request.GET.get('password')
	        resultado =confirmarLoginFuncionario(user,password,ano)
	        if resultado:
	        	resultado = confirmarLoginFuncionario(user,password,ano)
	        	request.session['user']=user
	        	request.session['password']=password
	        	for i in range (len(resultado)):
	        		request.session['id_user'] = resultado[i]['CodFuncionario']
	        		professor=carregarFuncionarios(request.session['id_user'])
	        	template='iniciop.html'
			request.session['usuario_activo']=professor[0]['Nome']
			return HttpResponseRedirect('/professores/')
	        elif request.GET.get('email') and request.GET.get('password'):	
	         	resultado='Utilizador ou password incorrectos'
			resultado='Utilizador ou password incorrectos'
	         	return render (request, template,{'resultado':resultado})
	else:
		a=2
	return  render(request, template)	  

