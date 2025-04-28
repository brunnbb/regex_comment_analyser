from extrator_e_analisador.crawler import AdoroCinema
from extrator_e_analisador.analisador import Analisador

def main():
    filme = input('Digite o código do filme, conforme listado na barra de endereço do site https://www.adorocinema.com/: ')
    n = int(input('Digite quantas páginas de comentários você deseja consultar: '))

    crawler = AdoroCinema()
    sinopse = crawler.extrairSinopseFilme(filme)
    crawler.salvarSinopseFilme(filme, sinopse)
    comentarios = crawler.extrairComentariosFilme(filme, n)
    crawler.salvarComentariosFilme(filme, comentarios)
    
    analisador = Analisador()
    resultados = analisador.analisar_paginas(comentarios)
    analisador.gerar_estatisticas(resultados)
    analisador.gerar_arquivo_resultados(filme, resultados, comentarios)
    
    print("\nPrograma executado com sucesso.")
    print(f"Consulte os arquivos '{filme}_comentarios.txt', '{filme}_comentarios_classificados.txt e '{filme}_sinopse.txt' na pasta arquivos.")
    
if __name__ == "__main__":
    main()
    