from django.shortcuts import render

# Função de índice que renderiza a página inicial da enciclopédia
def index(request):
    return render(request, 'encyclopedia/index.html')  # Renderiza o template `index.html`

# Exemplo de outras funções que podem estar neste arquivo
def entry(request, entry):
    return render(request, 'encyclopedia/entry.html', {'entry': entry})

def newPage(request):
    return render(request, 'encyclopedia/new_page.html')

def edit(request, entry):
    return render(request, 'encyclopedia/edit.html', {'entry': entry})

def randomPage(request):
    return render(request, 'encyclopedia/random.html')
