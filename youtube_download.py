#Importação De Bibliotecas
from pytube import YouTube
import moviepy.editor as moviepy
import re
import os
from threading import Thread

#Importação De Arquivos
import interface

#Função a ser executada quando o botão "Download" for pressionado
def downloadExecute():
    link = interface.linkBox.get()

    path = interface.directoryVar.get()

    #Tratamento de erro para o link inválido
    try:
        youtube = YouTube(link)
    except:
        interface.messagebox.showerror(title="Link Inválido!", message="O link inserido é inválido! Verifique se o link foi copiado corretamente e tente o download novamente.")
        exit()

    vq = interface.vquality.get()

    #Desabilita o botão de download durante o download e roda a progressBar
    interface.buttonDownload.config(state='disabled')
    interface.progressBar.start()

    #Exibe uma mensagem para o usuário
    interface.videoTitle.set("Aguarde... Download Em Andamento!")

    #Condição que verifica o RadioButton selecionado
    if (vq == 1):
        maxResolution = youtube.streams.get_highest_resolution()
        maxResolution.download(path)
    else:
        if (vq == 2):
            lowResolution = youtube.streams.get_lowest_resolution()
            lowResolution.download(path)
        else:
            if (vq == 3):
                audioOnly = youtube.streams.filter(only_audio=True).first()
                audioOnly.download(path)

                title = youtube.title

                #Localiza o MP4 baixado e converte em MP3
                for file in os.listdir(path):
                    if re.search('mp4', file):
                        mp4 = os.path.join(path, file)
                        mp3 = os.path.join(path, os.path.splitext(title)[0]+'.mp3')

                        newFile = moviepy.AudioFileClip(mp4)
                        newFile.write_audiofile(mp3)

                        os.remove(path + f'/{title}.mp4')

    #Exibe o título e o autor do vídeo baixado para o usuário ao final do download
    interface.videoTitle.set(f"Você baixou: {youtube.title} de {youtube.author}")

    #Finaliza a execução da progressBar após o download e habilita o botão novamente
    interface.progressBar.stop()
    interface.buttonDownload.config(state='normal')

#Cria uma função para a execução de download em uma Thread separada da função de download
def downloadFunction():
    Thread(target= downloadExecute).start()