# Python Tools

## PIPX

**Pipx** é ideal para instalar e gerenciar aplicativos de linha de comando (CLI) de forma isolada.  

Ele cria ambientes virtuais para cada ferramenta (como black, poetry, ruff), evitando conflitos de dependências. 

Use pipx quando precisar de ferramentas CLI sem poluir o ambiente global. 



## PYENV

**Pyenv** gerencia versões do Python no seu sistema.  

Permite instalar, alternar e usar diferentes versões do Python (como 3.8, 3.11, 3.12) em projetos distintos. 

Use pyenv para garantir que cada projeto use a versão correta de Python. 


> **_NOTE:_**
Use o comando pyenv local <versão> dentro do diretório do projeto para definir uma versão específica do Python.
Isso cria um arquivo .python-version no projeto, garantindo que a versão correta seja usada 
sempre que você entrar no diretório.
Assim, cada projeto pode ter sua própria versão isolada do Python.

Execute:

```bash
pyenv --version
pyenv install 3.14
pyenv local 3.14
```

## POETRY

**Poetry** é uma ferramenta completa para gestão de dependências, ambientes virtuais, construção e publicação de pacotes.  

Ele lida com pyproject.toml, poetry.lock e cria ambientes isolados automaticamente. 

Use Poetry para desenvolver projetos Python com dependências bem definidas e controle de versão. 