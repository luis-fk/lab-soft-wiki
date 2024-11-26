# Como rodar o projeto
Para rodar o projeto basta clonar o repositório no seu computador. Você também precisara do [Python](https://www.python.org/) instalado no seu computador com versão 3.12 ou maior e [NodeJS](https://nodejs.org/en). Uma vez clonado o repositório você verá duas pastas pricipais, a `wiki-fe` e `wiki-be`.

### wiki-be
Na pasta `wiki-be` você irá encontrar o arquivo `requirements.txt` com todas as dependências necessárias para rodar o back-end na sua máquina. 

Recomendamos o uso do [poetry](https://python-poetry.org/docs/), que pode ser usado para instalar as dependências da seguinte maneira:

Na pasta `wiki-be` e com poetry instalado na sua máquina, execute:
- `poetry init`: configure as opções do projeto, pode aceitar todos os valores padrões recomendados pelo poetry.
- `Get-Content requirements.txt | ForEach-Object { poetry add $_ }`: isso instalará todas as depedencias do projeto.
- `poetry shell`
- `python manage.py runserver`: esse comando irá inciar o servidor.

### wiki-fe
Na pasta `wiki-fe` você ira encontar a parte do projeto relativa ao front-end do site. Basta entrar na pasta e executar os seguintes comandos:

- `npm install`
- `npm run dev`

Após isso é só entrar na url fornecida.