import requests
import json
import datetime
from TOKEN import TOKEN

class TelegramBot:
    def __init__(self):
        self.iURL = f"https://api.telegram.org/bot{TOKEN}/"

    def Iniciar(self):
        iUPDATE_ID = None
        while True:
            ATUALIZACAO = self.ler_novas_mensagens(iUPDATE_ID)
            IDADOS = ATUALIZACAO["result"]
            if IDADOS:
                for dado in IDADOS:
                    iUPDATE_ID = dado['update_id']
                    if "message" in dado and "new_chat_members" in dado["message"]:
                        self.handle_new_members(dado["message"])

    def ler_novas_mensagens(self, iUPDATE_ID):
        iLINK_REQ = f'{self.iURL}getUpdates?timeout=5'
        if iUPDATE_ID:
            iLINK_REQ = f'{iLINK_REQ}&offset={iUPDATE_ID + 1}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)

    def handle_new_members(self, message):
        chat_id = message["chat"]["id"]
        chat_info = self.get_chat_info(chat_id)
        chat_title = chat_info.get("title", "N/A")
        admins = self.get_chat_administrators(chat_id)
        members_count = self.get_chat_members_count(chat_id)

        admin_usernames = [admin["user"]["username"] for admin in admins if "username" in admin["user"]]
        admin_usernames_str = ', '.join(admin_usernames)

        welcome_message = f"""
        😃 OLÁ! FUI ADICIONADO AO GRUPO. VAMOS VER ALGUMAS ESTATÍSTICAS:
        <b>🆔 ID DO GRUPO:</b> <code>{chat_id}</code>
        <b>🏷 NOME DO GRUPO:</b> <code>{chat_title}</code>
        <b>🔗 URL:</b> <code>{chat_info.get('invite_link', 'N/A')}</code>
        <b>👮 ADMINISTRADORES:</b> <code>{admin_usernames_str}</code>
        <b>📊 QUANTIDADE DE MEMBROS:</b> <code>{members_count}</code>
        <b>📅 DATA:</b> <code>{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</code>
        """
        self.send_message(chat_id, welcome_message)

    def get_chat_info(self, chat_id):
        iLINK_REQ = f'{self.iURL}getChat?chat_id={chat_id}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)["result"]

    def get_chat_administrators(self, chat_id):
        iLINK_REQ = f'{self.iURL}getChatAdministrators?chat_id={chat_id}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)["result"]

    def get_chat_members_count(self, chat_id):
        iLINK_REQ = f'{self.iURL}getChatMembersCount?chat_id={chat_id}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)["result"]

    def send_message(self, chat_id, text):
        iLINK_REQ = f'{self.iURL}sendMessage?chat_id={chat_id}&text={text}&parse_mode=html'
        requests.get(iLINK_REQ)

bot = TelegramBot()
bot.Iniciar()
