from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


from .models import Estado, Cidade, Campus, Servidor, Status, Situacao, Classe, Progressao, Campo, Atividade, Comprovante, Validacao

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

from django.shortcuts import get_object_or_404
from .models import Cidade
from cadastros.forms import ComprovanteForm

# Create your views here.


def editar_cidade(request, pk):
    cidade = get_object_or_404(Cidade, pk=pk)
    if request.method == 'POST':
        # Lógica para salvar as alterações da cidade
        cidade.save()
        return redirect('listar-cidade')
    return render(request, 'paginas/cidade_form.html', {'cidade': cidade})

class CampusCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Campus
    fields = ['cidade', 'endereco', 'telefone']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-campus')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Cadastro de Campus"
        context['botao'] = "Cadastrar"
        context['icone'] = '<i class="fa fa-check" aria-hidden="true"></i>'

        return context


class StatusCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Status
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-status')


class SituacaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Situacao
    fields = ['status', 'detalhes']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-situacao')


class ClasseCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Classe
    fields = ['nome', 'nivel', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-classe')


class ProgressaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Progressao
    fields = ['classe', 'data_inicial', 'data_final', 'observacao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-progressao')

    def form_valid(self, form):

        # Antes do super não foi criado o objeto nem salvo no banco
        form.instance.usuario = self.request.user

        url = super().form_valid(form)

        return url


class CampoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Campo
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-campo')


class AtividadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['campo', 'numero', 'descricao', 'pontos', 'detalhes']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-atividade')


class ComprovanteCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Comprovante
    form_class = ComprovanteForm
    template_name = 'cadastros/form-upload.html'
    success_url = reverse_lazy('listar-comprovante')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        arquivos = self.request.FILES.getlist('arquivo')
        quantidade = form.cleaned_data.get('quantidade')
        data = form.cleaned_data.get('data')
        atividade = form.cleaned_data.get(
            'atividade')  # Captura o valor da atividade

        # Cria um objeto Comprovante para cada arquivo enviado
        for arquivo in arquivos:
            Comprovante.objects.create(
                usuario=self.request.user,
                atividade=atividade,  # Adiciona a atividade aqui
                arquivo=arquivo,
                quantidade=quantidade,
                data=data,
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['botao'] = 'Cadastrar'
        context['arquivos'] = Comprovante.objects.filter(
            usuario=self.request.user)  # Busca todos os arquivos do usuário
        return context


class ValidacaoCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Validacao
    fields = ['quantidade', 'justificativa']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-validacoes')


################# UPDATE #################

class CampusUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Campus
    fields = ['cidade', 'endereco', 'telefone']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-campus')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = "Editar cadastro de Campus"
        context['botao'] = "Salvar"

        return context


class ServidorUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Servidor
    fields = ['nome_completo', 'siape', 'cpf', 'campus']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('index')


class StatusUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Status
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-status')


class SituacaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Situacao
    fields = ['status', 'detalhes']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-situacao')


class ClasseUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Classe
    fields = ['nome', 'nivel', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-classe')


class ProgressaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Progressao
    fields = ['classe', 'data_inicial', 'data_final', 'observacao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-progressao')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Progressao, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class CampoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Campo
    fields = ['nome', 'descricao']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-campo')


class AtividadeUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Atividade
    fields = ['campo', 'numero', 'descricao', 'pontos', 'detalhes']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-atividade')


class ComprovanteUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Comprovante
    fields = ['progressao', 'atividade', 'quantidade', 'data', 'data_final', 'arquivo']
    template_name = 'cadastros/form-upload.html'
    success_url = reverse_lazy('listar-comprovante')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Comprovante, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['botao'] = 'Salvar'
        return context


class ValidacaoUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Validacao
    fields = ['quantidade', 'justificativa']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-validacoes')

    


################# DELETE #################


class CampusDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Campus
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-campus')


class StatusDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-status')


class SituacaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-situacao')


class ClasseDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Classe
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-classe')


class ProgressaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Progressao
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-progressao')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Progressao, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class CampoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Campo
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-campo')


class AtividadeDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-atividade')


class ComprovanteDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Comprovante
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-comprovante')


class ValidacaoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Validacao
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-validacao')


################# LISTA #################


class EstadoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Estado
    template_name = 'cadastros/listas/estados.html'


class CidadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Cidade
    template_name = 'cadastros/listas/cidades.html'
    paginate_by = 10

    def get_queryset(self):

        txt_nome = self.request.GET.get('nome')

        if txt_nome:
            cidades = Cidade.objects.filter(nome__icontains=txt_nome)
        else:
            cidades = Cidade.objects.all()

        return cidades


class CampusList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Campus
    template_name = 'cadastros/listas/campus.html'


class StatusList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Status
    template_name = 'cadastros/listas/status.html'


class SituacaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Situacao
    template_name = 'cadastros/listas/situacao.html'


class ClasseList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Classe
    template_name = 'cadastros/listas/classe.html'


class ProgressaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Progressao
    template_name = 'cadastros/listas/progressao.html'

    def get_queryset(self):
        self.object_list = Progressao.objects.filter(usuario=self.request.user)
        return self.object_list


class CampoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Campo
    template_name = 'cadastros/listas/campo.html'


class AtividadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Atividade
    template_name = 'cadastros/listas/atividade.html'


class ComprovanteList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Comprovante
    template_name = 'cadastros/listas/comprovante.html'


class ValidacaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Validacao
    template_name = 'cadastros/listas/validacao.html'
