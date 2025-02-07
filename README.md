# :video_game: Jogo Personalizado para Minha Filha
Este é um jogo especial desenvolvido em Python usando o Framework Kivy e a biblioteca interna do python radom, e a ferramenta buildozer. 
O projeto foi criado como um presente para minha filha, proporcionando uma experiência divertida e educativa.

O desenvolvimento foi inspirado no tutorial do programador Sr. Jonathan, publicado no canal do YouTube freeCodeCamp.org. 
Você pode conferir o tutorial completo neste link: [Tutorial do Jogo Galaxy.](https://www.youtube.com/watch?v=l8Imtec4ReQ&list=PLIfnysyBPjWyDvEihlxPeNsTGhbp1NrzR&index=4)


# 🚀 Tecnologias Utilizadas
- **Python**
- **Kivy** (Interface gráfica)
- **radom**
- **Outros Ferramentas:**
  - **Buildozer** (Ferrameta de empacotar aplicativos para executarem em plataformas mobile)
 
# 🎲 Como Jogar
## 1. Clone o repositório:
```bash
git clone https://github.com/zantech-pro/joguinho_da_emanuela.git
```
## 2. Criar e Ativar um Ambiente Virtual (Opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```
## 3. Instale as dependências:
```bash
pip install -r requirements.txt
```
## 4. Execute o jogo:
```bash
python main.py
```
# 🖥️ Capturas de Tela
![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](Joguinho_da_Emanuela_v1/img/tela1.png)

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](Joguinho_da_Emanuela_v1/img/tela2.png)


# Estrutura do Projeto
```mermaid
flowchart TD
    subgraph root
        dir1[Joguinho_da_Emanuela_v1/]
        dir2[audio]
        dir3[fonts]
        dir4[img]
        file1[**Arquivo principal**
        main.py]
        file2[**Trata I/O dos usuario no touch ou teclado**
        acoes_usuarios.py]
        file3[**Dependências do projeto**
        requirements.txt ]
        file4[**Documentação do projeto**
        README.md]
        file5[**Parametros para Buildozer convereter Mobile**
        buildozer.spec]
        file6[**Estruturação de layout na liguagem Kivy**
        joguinhodaemanuela.kv]
        file7[**Arquivo que trabalha em conjunto ao menu.kv, defini as opções para usuario**
        menu.py]
        file8[**Trata perpectiva 2D e perpectiva foco em profudidade**
        menu.py]
    end
    
    dir1 --> dir2
    dir1 --> dir3
    dir1 --> dir4
    dir1 --> file1
    dir1 --> file2
    dir1 --> file3
    dir1 --> file4
    dir1 --> file5
    dir1 --> file6
    dir1 --> file7
    dir1 --> file8
    root --> dir1
```
📌 Funcionalidades
✅ Interface interativa e amigável
✅ Mecânica divertida e educativa
✅ Totalmente personalizado

📜 Licença
Este projeto foi feito com carinho e é de uso pessoal. Caso tenha interesse, entre em contato!

Meu telegram: [@zandermais](https://t.me/zandermais)

📧: dev@zantech.com.br


