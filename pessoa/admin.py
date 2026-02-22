from django.contrib import admin
from .models import Pessoa, PessoaFisica, PessoaJuridica, Contato

admin.site.register(Pessoa)
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
admin.site.register(Contato)
