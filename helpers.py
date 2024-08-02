import os
from tkinter import filedialog, Listbox, END
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import html

from resources import get_resource_path, chunk_list

json_path = get_resource_path('conta-de-servico.json')
credentials = service_account.Credentials.from_service_account_file(json_path)
client = translate.Client(credentials=credentials)

def select_files(file_listbox: Listbox):
    filetypes = [("Arquivos permitidos", "*.js *.py *.r")]
    
    file_paths = filedialog.askopenfilenames(title="Selecione os arquivos", filetypes=filetypes)
    
    #file_listbox.delete(0, END)
    
    for file_path in file_paths:
        file_listbox.insert(END, file_path)

def delete_selected(file_listbox: Listbox, event=None):
    # Obter a seleção atual
    selected_indices = file_listbox.curselection()
    for index in reversed(selected_indices):
        file_listbox.delete(index)

def extract_comments_from_file(file_path: str):
    comments = []
    _, ext = os.path.splitext(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if (ext == ".py" or ext == ".r") and "#" in line:
                comments.append((line_num, line))
            elif ext == ".js" and ("//" in line or "/*" in line):
                comments.append((line_num, line))
    return comments

def update_file_with_translations(file_path: str, translated_comments: list[tuple], lang: str):
    dir_name, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)
    new_file_name = f"{name}_{lang}{ext}"
    new_file_path = os.path.join(dir_name, new_file_name)    

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Atualizar as linhas com os comentários traduzidos
    with open(new_file_path, "w", encoding="utf-8") as file:
        for i, line in enumerate(lines):
            for comment_line_num, translated_comment in translated_comments:
                translated_comment = html.unescape(translated_comment)
                if i == comment_line_num - 1:
                    if(ext == ".py" or ext == ".r"):
                        if line.startswith("#"):
                            file.write(f"{translated_comment}")
                            break    
                        elif "#" in line:
                            parts = line.split("#", 1)
                            file.write(f"{parts[0]}{translated_comment}")                            
                            break   
                    elif ext == ".js":
                        if line.startswith("//") or line.startswith("/*"):
                            file.write(f"{translated_comment}")
                            break
                        elif "//" in line:
                            parts = line.split("//", 1)
                            file.write(f"{parts[0]}{translated_comment}")                            
                            break
                        elif "/*" in line:
                            parts = line.split("/*", 1)
                            file.write(f"{parts[0]}{translated_comment}")                            
                            break

            else:
                file.write(line)

def process_listbox(file_listbox: Listbox, lang: str):
    files = file_listbox.get(0, END)
    fixed_comment = "Atenção: A tradução dos comentários desse arquivo foram geradas automaticamente por Inteligência Artificial"
    first_comment = True
    for file in files:
        comments = extract_comments_from_file(file)
        
        comment_texts = []
        for _, comment in comments:
            # adiciona mensagem fixa no primeiro comentario
            if first_comment == True:
                comment = f'{comment} | {fixed_comment} \n'
                first_comment = False

            if comment.startswith("#") or comment.startswith("//") or comment.startswith("/*"):
                comment_texts.append(comment)      
            else:
                if "#" in comment:
                    parts = comment.split("#", 1)
                    comment_texts.append(f"# {parts[1]}")
                elif "//" in comment:
                    parts = comment.split("//", 1)
                    comment_texts.append(f"// {parts[1]}")
                elif "/*" in comment and "*/" in comment:
                    start_idx = comment.find("/*")
                    end_idx = comment.find("*/")
                    comment_texts.append(f"/* {comment[start_idx+2:end_idx]} */") 
        
        chunk_size = 128
        translated_comments = []

        for chunk in chunk_list(comment_texts, chunk_size):
            translations = client.translate(values=chunk, target_language=lang)
            translated_comments.extend(translations)

        translated_comments = [(comments[i][0], translated_comments[i]["translatedText"]) for i in range(len(translated_comments))]
        update_file_with_translations(file, translated_comments, lang)
        
    