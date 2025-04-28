from extrator_e_analisador.analisador import Analisador

a = ['Filme não é bom mas incrível',
     'Filme ruim',
     'Filme mediocre',
     'Filme com bons momentos mas genérico']
analisador = Analisador() 
r = analisador.analisar_paginas(a)
print(r)