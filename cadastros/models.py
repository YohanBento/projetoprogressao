from django.db import models
from django.contrib.auth.models import User

# Métodos e Choices


def user_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'usuario_{0}/{1}'.format(instance.user.id, filename)


# Classes (modelos)

class Estado(models.Model):
    nome = models.CharField(max_length=50)
    uf = models.CharField(max_length=2, verbose_name='UF')

    def __str__(self):
        return "{}".format(self.uf)


class Cidade(models.Model):
    nome = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.nome)


class Campus(models.Model):
    cidade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=150, verbose_name="endereço")
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return "{} ({})".format(self.nome, self.descricao)


class Servidor(models.Model):
    nome_completo = models.CharField(max_length=100)
    siape = models.CharField(max_length=10)
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)
    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="usuário")


class Status(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150, verbose_name="descrição")

    def __str__(self):
        return "{} ({})".format(self.nome, self.descricao)


class Situacao(models.Model):
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    movimentado_em = models.DateTimeField(auto_now_add=True)
    movimentado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    detalhes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} em {} por {}".format(self.status, self.movimentado_em, self.movimentado_por)


class Classe(models.Model):
    nome = models.CharField(max_length=50)
    nivel = models.IntegerField(verbose_name="nível")
    descricao = models.CharField(max_length=150, verbose_name="descrição", null=True, blank=True)

    def __str__(self):
        return "{} nível {}".format(self.nome, self.nivel)


class Progressao(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    data_inicial = models.DateField()
    data_final = models.DateField()
    observacao = models.TextField()
    # Relaciona com o servidor
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.classe} - {self.usuario}"


class Campo(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150, verbose_name="descrição")

    def __str__(self):
        return "{} ({})".format(self.nome, self.descricao)


class Atividade(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Comprovante(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    atividade = models.ForeignKey(
        Atividade, on_delete=models.CASCADE)  # Campo obrigatório
    arquivo = models.FileField(upload_to='uploads/')
    quantidade = models.IntegerField()
    data = models.DateField()

    def __str__(self):
        return f"{self.usuario} - {self.atividade} - {self.data}"


class Validacao(models.Model):
    comprovante = models.ForeignKey(Comprovante, on_delete=models.PROTECT)
    validado_em = models.DateTimeField(auto_now_add=True)
    validado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    quantidade = models.DecimalField(decimal_places=2, max_digits=5)
    justificativa = models.TextField(max_length=255)

    def __str__(self):
        return "[{}] Pontuação: {}/{} por {}".format(self.comprovante.pk, self.quantidade, self.comprovante.quantidade, self.validado_por)
