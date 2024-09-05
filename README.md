# Instalação do FFmpeg

Este projeto requer o **FFmpeg** para funcionar corretamente. O FFmpeg é uma ferramenta de linha de comando usada para manipulação de arquivos de mídia, como áudio e vídeo. Ele é necessário para baixar e converter músicas no formato correto durante a execução do programa.

## Instruções para Instalação do FFmpeg no Windows

Siga os passos abaixo para instalar e configurar o FFmpeg no Windows:

### Passo 1: Baixar o FFmpeg

1. Acesse o site oficial para baixar o FFmpeg:
   [Download FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/#release-builds)

2. Na seção **Release Builds**, clique no link para **Download FFmpeg** em `ffmpeg-release-full.7z`. Este é o pacote essencial para a maioria dos usuários.

3. Após o download, extraia o conteúdo do arquivo `.zip` em um diretório de sua escolha. Recomendo algo como `C:\ffmpeg` para facilitar o acesso.

### Passo 2: Adicionar FFmpeg ao Caminho (PATH) do Sistema

Para que o FFmpeg possa ser usado em qualquer lugar no seu sistema, você deve adicionar o diretório `bin` ao **PATH** do Windows:

1. **Abra as Configurações Avançadas do Sistema**:
   - Clique com o botão direito em **Este Computador** (ou **Meu Computador**) e selecione **Propriedades**.
   - No lado esquerdo, clique em **Configurações Avançadas do Sistema**.

2. **Configurar Variáveis de Ambiente**:
   - Na janela **Propriedades do Sistema**, clique no botão **Variáveis de Ambiente**.

3. **Editar o PATH**:
   - Na seção **Variáveis do Sistema**, encontre a variável `Path`, selecione-a e clique em **Editar**.
   - Na janela de edição, clique em **Novo** e adicione o caminho completo para a pasta `bin` do FFmpeg.
     - Exemplo: `C:\ffmpeg\bin`

4. **Salvar as alterações**:
   - Clique em **OK** para fechar todas as janelas e salvar as alterações.

### Passo 3: Verificar a Instalação do FFmpeg

1. Abra o **Prompt de Comando** ou o **PowerShell**.
2. Digite o seguinte comando para verificar se o FFmpeg foi instalado corretamente:

   ```bash
   ffmpeg -version
