import requests
from bs4 import BeautifulSoup

class AdoroCinema:

    def extrairSinopseFilme(self, filme):      
        url = "https://www.adorocinema.com/filmes/" + filme + '/'
        htmlFilme = requests.get(url).text
        bsS = BeautifulSoup(htmlFilme, 'html.parser')
        sinopse = bsS.find('div', class_="content-txt").get_text(strip=True) # type: ignore
        return sinopse
    
    def salvarSinopseFilme(self, filme, sinopse):
        with open('arquivos/' + filme + '_sinopse.txt', 'w', encoding='utf-8') as f:
            f.write(sinopse)

    def extrairComentariosFilme(self, filme, n):
        comentarios = []
        for i in range(1, n + 1):
            url = f'http://www.adorocinema.com/filmes/{filme}/criticas/espectadores/?page={i}'
            htmlComentarios = requests.get(url).text
            bsC = BeautifulSoup(htmlComentarios, 'html.parser')
            comentarios_com_tags = bsC.find_all('div', class_="content-txt review-card-content")
            for comentario_com_tag in comentarios_com_tags:
                comentarios.append(comentario_com_tag.get_text().strip())
        return comentarios

    def salvarComentariosFilme(self, filme, comentarios):
        with open('arquivos/' + filme + '_comentarios.txt', 'w', encoding='utf-8') as f:
            for comentario in comentarios:
                f.write(comentario + '\n\n')
