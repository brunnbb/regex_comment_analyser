import re
from arquivos.dicionario import adjetivos, adverbios


class Analisador:
    def __init__(self) -> None:
        self.padrao_palavra = re.compile(r"\b\w{3,}\b")
        self.padrao_adv_adj = re.compile(
            r"\b(?:"
            + "|".join(adverbios.keys())
            + r")\s+(?:"
            + "|".join(adjetivos.keys())
            + r")\b|\b(?:"
            + "|".join(adjetivos.keys())
            + r")\b"
        )

    def simplificar_comentarios(self, comentarios: list[str]):
        return [" ".join(self.padrao_palavra.findall(comentario.lower())) for comentario in comentarios]

    def analisar_comentario(self, comentario: str):
        palavras_encontradas = self.padrao_adv_adj.findall(comentario)

        pontuacao_total = 0
        num_palavras = 0
        
        for palavra in palavras_encontradas:

            if palavra in adjetivos:
                pontuacao_total += adjetivos[palavra]
                num_palavras += 1

            elif palavra in adverbios:
                continue

            elif " " in palavra:
                partes = palavra.split()
                if len(partes) == 2:
                    adv, adj = partes
                    if adv in adverbios and adj in adjetivos:
                        pontuacao_total += adjetivos[adj] * adverbios[adv]
                        num_palavras += 1

        if num_palavras > 0:
            pontuacao_media = pontuacao_total / num_palavras
        else:
            pontuacao_media = 0

        if pontuacao_media > 0.05:
            return 'POSITIVO'
        elif pontuacao_media < -0.05:
            return 'NEGATIVO'
        else:
            return 'NEUTRO'

    def analisar_paginas(self, comentarios: list[str]):
        comentarios_simplificados = self.simplificar_comentarios(comentarios)
        return [self.analisar_comentario(comentario) for comentario in comentarios_simplificados]

    def gerar_estatisticas(self, resultados):
        total = len(resultados)
        positivos = resultados.count("POSITIVO")
        negativos = resultados.count("NEGATIVO")
        neutros = resultados.count("NEUTRO")

        print(f"Total de Comentários: {total}")
        print(f"Positivos: {positivos} ({positivos / total * 100:.2f}%)")
        print(f"Negativos: {negativos} ({negativos / total * 100:.2f}%)")
        print(f"Neutros: {neutros} ({neutros / total * 100:.2f}%)")

    def gerar_arquivo_resultados(self, filme, resultados, comentarios):
        with open("arquivos/" + filme + "_comentarios_classificados.txt", "w", encoding="utf-8") as f:
            for comentario, resultado in zip(comentarios, resultados):
                f.write(f"[{resultado}] {comentario}\n\n")
