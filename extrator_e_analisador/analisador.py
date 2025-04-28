import re
from arquivos.dicionario import adjetivos, adverbios

class Analisador:
    def __init__(self) -> None:
        self.padrao_palavra = re.compile(r'\b\w{3,}\b')
        self.padrao_adv_adj = self.padrao_adv_adj = re.compile(r'\b(?:' + '|'.join(adverbios.keys()) + 
                                                               r')\s+(?:' + '|'.join(adjetivos.keys()) + 
                                                               r')\b|\b(?:' + '|'.join(adjetivos.keys()) + 
                                                               r')\b')
    
    def simplificar_comentarios(self, comentarios: list[str]):
        comentarios_processados = []

        for comentario in comentarios:
            palavras_filtradas = self.padrao_palavra.findall(comentario.lower())
            comentarios_processados.append(" ".join(palavras_filtradas))

        return comentarios_processados
        
    def analisar_comentario(self, comentario: str):
        palavras_encontradas = self.padrao_adv_adj.findall(comentario.lower())

        pontuacao_total = 0
        num_palavras = 0
        
        i = 0
        while i < len(palavras_encontradas):
            palavra = palavras_encontradas[i].strip()

            # Se a palavra for um advérbio seguido de um adjetivo
            if palavra in adverbios:
                # A próxima palavra deve ser um adjetivo
                if i + 1 < len(palavras_encontradas):
                    proxima_palavra = palavras_encontradas[i + 1].strip()
                    if proxima_palavra in adjetivos:
                        pontuacao_total += adjetivos[proxima_palavra] * adverbios[palavra]
                        num_palavras += 1
                        i += 2  # Pular a próxima palavra (o adjetivo)
                        continue

            # Caso a palavra seja apenas um adjetivo
            elif palavra in adjetivos:
                pontuacao_total += adjetivos[palavra]
                num_palavras += 1

            i += 1  

        if num_palavras > 0:
            pontuacao_media = pontuacao_total / num_palavras
        else:
            pontuacao_media = 0

        if pontuacao_media > 0.1:
            return 'POSITIVO'
        elif pontuacao_media < -0.1:
            return 'NEGATIVO'
        else:
            return 'NEUTRO'

    def analisar_paginas(self, comentarios: list[str]):
        comentarios_simplificados = self.simplificar_comentarios(comentarios)
        resultados = []
        for comentario in comentarios_simplificados:
            resultado = self.analisar_comentario(comentario)
            resultados.append(resultado)
        return resultados
    
    def gerar_estatisticas(self, resultados):
        total = len(resultados)
        positivos = resultados.count('POSITIVO')
        negativos = resultados.count('NEGATIVO')
        neutros = resultados.count('NEUTRO')

        print(f"Total de Comentários: {total}")
        print(f"Positivos: {positivos} ({positivos / total * 100:.2f}%)")
        print(f"Negativos: {negativos} ({negativos / total * 100:.2f}%)")
        print(f"Neutros: {neutros} ({neutros / total * 100:.2f}%)")

    def gerar_arquivo_resultados(self, filme, resultados, comentarios):
        with open('arquivos/' + filme + '_comentarios_classificados.txt', 'w', encoding='utf-8') as f:
            for comentario, resultado in zip(comentarios, resultados):
                f.write(f"[{resultado}] {comentario}\n\n")
