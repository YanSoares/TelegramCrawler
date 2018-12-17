# IMPORTS
import telebot
import dontpad
import re

# ID DO TELEGRAM DESTINO
telegram_destino = 364276001

# TOKEN GERADO PELA BOTFATHER DO TELEGRAM
token = "611032927:AAG9jxBgvaiKM-EvJQ7Z2j28IlLRZ1I65GA"

# ATRIBUINDO À VARIAVEL bot O NOSSO BOT CRIADO PELO BOTFATHER
bot = telebot.TeleBot(token)

print("INICIADO COM SUCESSO!!!")

# FILTRANDO MENSAGENS DO TIPO DOCUMENTO E ENCAMINHANDO PARA O TELEGRAM DESTINO
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    bot.forward_message(telegram_destino, message.chat.id, message.message_id)
    print("\n\nDOC IDENTIFICADO: ")
    print(message.document.file_name)


    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('/home/yansoares/Dropbox/DSB_ARQUIVOS/'+ message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

# FILTRANDO MENSAGENS DO TIPO URL E ENCAMINHADO PARA O TELEGRAM DESTINO ALEM DE ATUALIZAR O REPOSITORIO
@bot.message_handler(regexp='((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
def handle_message(message):
    #bot.send_message(telegram_destino, message.text)

    #PEGA SOMENTE O LINK DA MENSAGEM E GUARDA NA VARIAVEL M (NA POSICAO 0)
    m = re.search('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', message.text)

    # PEGANDO O LINK NOVO E ATUALIZANDO O ARQUIVO
    # Abra o arquivo (leitura)
    arquivo = open('links.txt', 'r')
    conteudo = arquivo.readlines()
    # insira seu conteúdo
    # obs: o método append() é proveniente de uma lista
    conteudo.append("\n\n" + m.group(0))
    # Abre novamente o arquivo (escrita) e escreva o conteúdo criado anteriormente nele.
    arquivo = open('links.txt', 'w')
    arquivo.writelines(conteudo)
    arquivo.close()

    # MANDANDO O TEXTO DO ARQUIVO PARA O DONTPAD
    texto = ""
    manipulador = open('links.txt', 'r')
    for linha in manipulador:
        texto += linha
    manipulador.close()
    dontpad.write("dsb_bot", texto)
    print("\n\nmensagem: " + message.text + "\nid da mensagem: " + str(message.message_id) + "\ntipo de mensagem: " + message.chat.type + "\nLINK IDENTIFICADO: " + m.group(0))


# FILTRANDO OUTROS TIPOS DE MENSAGENS, PEGANGO OS DADOS REFERENTE A MENSAGEM SOMENTE PARA OBSERVAÇÃO (LOG)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("\n\nmensagem: " + message.text + "\nid da mensagem: " + str(message.message_id) + "\ntipo de mensagem: " + message.chat.type)


# INICIANDO O BOT
bot.polling()
