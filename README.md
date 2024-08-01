# Sobre
Este projeto é um simples app desktop escrito em Python com TKinter e compilado com pyinstaller. 

## Motivação
Ele uniu minha vontade de trabalhar com Python desktop e a necessidade de criar um sistema de tradução de comentários de arquivos de código fonte dos tipos Python, R e JavaScript.

# Executar o projeto
- ative o ambiente virtual através do script activate
  - no windows execute: `virtual-env\Scripts\activate.bat`  
- faça a instalação das depêndencias através do **requirements.txt** através do comando `pip install -r requirements.txt`
- tenha o arquivo `conta-de-servico.json` na raíz do projeto, que representa uma conta de serviço de um projeto Google Cloud.
- execute o projeto no modo sem debug (Ctrl + F5)
> Se tudo correr bem, a do programa deve aparecer.

## Criação da conta de serviço
Para criar uma conta de serviço você deve ter uma conta do Google Cloud que possa criar um projeto. Após a criação do projeto vá até https://console.cloud.google.com/iam-admin/serviceaccounts?authuser=1&project={ID-DO-PROJETO} e clique para criar uma nova conta de serviço. Dê um nome e defina a descrição. Após isso, é importante setar o papel **Usuário da API Cloud Translation** para que seja possível acionar a API de tradução corretamente.

# Funcionamento
Com o projeto em execução, basta clicar no botão `Selecionar Arquivos`, selecione um ou mais arquivos, caso tenha selecionado algum arquivo equivocadamente, basta clicar no arquivo que está na lsita e depois pressionar a tecla `Delete`. Caso os arquivos selecionados sejam os corretos, clique em `Traduzir Arquivos`. A Aplicação vai ter retornar um status assim que a tradução for concluída.

![image](https://github.com/user-attachments/assets/4ba0113c-e349-4ae2-9f5b-c34d3b3a466f)

# Compilar o projeto
Para compilar o projeto, utilize o comando `pyinstaller tradutor-de-comentarios.spec`. Se tudo correr bem, uma pasta chamada `dist` deve ser criada com o executável.

# Resultado
Ainda há muito que melhorar, como por exemplo, comentários em bloco em arquivos JavaScript utilizando `/**/`.

## Arquivo original
![image](https://github.com/user-attachments/assets/18078583-a71d-43a4-92b0-10c3caa4c08c)

## Traduzido para inglês
![image](https://github.com/user-attachments/assets/68e43155-60e5-441f-8519-6825013017f4)

## Traduzido para espanhol
![image](https://github.com/user-attachments/assets/96a1911f-5eac-4c94-8c8d-8d00f0a467fd)

