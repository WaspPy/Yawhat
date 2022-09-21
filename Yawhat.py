###### ================================================================================================= ######
###### ================================================================================================= ######
###### ============================================ Yamwhat ============================================ ######
###### ================================================================================================= ######
###### ================================================================================================= ######
###### =========== Yamwhat is part of a project to forward Yammer msg and files to whatsapp ============ ######
###### = In order to use this you got to install Yampy, authenticator,Pywhatkit, pdf2img and pypiwin32 = ######
###### ============ I had to use pdf2img because we cannot find an easy solution to send pdf =========== ######
###### ============ files in whatsapp, futur will tell if we manage to implement new cmd in  =========== ######
###### =========================================== pywhatkit =========================================== ######
###### ================================================================================================= ######
###### ================================================================================================= ######
###### ===================================== SLT BLONDEL & SLT GIRE ==================================== ######
###### ================================================================================================= ######
###### ================================================================================================= ######

import pdf2image
import pywhatkit
import yampy
import requests
import requests.auth
import os
import urllib.parse
import time
import logging

def sdmsg(grp, msg):
    #   Fct send msg in whatsapp group
    #   grp => target grp to send img
    #   msg => Msg to send in str

    try:
        pywhatkit.sendwhatmsg_to_group_instantly(grp, msg, 20, True,2)  # Wait time>

        print("Success msg sending")
    except:
        print("Error msg sending")

    time.sleep(5)


def sdimg(grp, img_folder, img):
    #   Fct send img in whatsapp group
    #   grp => target grp to send img
    #   img_folder => Path to img folder with "/" and no "\"
    #   img => img name with extension
    #   img separated because flemme de coder du traitement du nom :*

    path_img = img_folder + img

    try:
        pywhatkit.sendwhats_image(grp, path_img, img.rstrip(".jpeg"), 20, True, 2)
        print("Success img sending")
    except:
        print("Error img sending")

    time.sleep(5)


def sdpdf(grp, pdf_folder, pdf, img_folder):
    #   Fct convert a pdf file in image for each page of th document then sending img using sdimg()
    #   grp => target grp to send pdf
    #   pdf_folder => Path to pdf folder with "/" and no "\" (or r"")
    #   pdf => pdf name with extension
    #   pdf separated because flemme de coder du traitement du nom :*
    #   img_folder destination folder to save img after conversion
    print("Sending pdf")
    pdf_path = pdf_folder + pdf
    pages = pdf2image.convert_from_path(pdf_path, poppler_path="C:/Users/Jbey/Documents/Cours/whatmer bot/Library/bin")

    for c, page in enumerate(pages):
        img_name = pdf.rstrip(".pdf") + "-P" + str(c + 1) + ".jpeg"
        page.save(img_folder + img_name, "JPEG")
        sdimg(grp, img_folder, img=img_name)


# Init

# Yammer var
access_token = '7259660-XUzvLF9bIEGjvXCjToBPQ'  # Mon token API
yammer = yampy.Yammer(access_token=access_token)
group_id = 117272174592

# Whatsapp var
pdf_fldr = "C:/Users/Jbey/Documents/CLEA21/Yawhat/Pdf_folder/"
pdf_name = "Rapport 220902.pdf"
img_flder = "C:/Users/Jbey/Documents/CLEA21/Yawhat/Img_folder/"
whtspp_grp = "L6HClqF9xdN6AyUSgkboTY"




logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("La fonction a bien été exécutée")
logging.info("Message d'information général")
logging.warning("Attention !")
logging.error("Une erreur est arrivée")
logging.critical("Erreur critique")


# Running part

while True:
    try:

        lst_msg_id = []
        for (repertoire, sousRepertoires, fichiers) in os.walk('timeline'):
            lst_msg_id.extend(sousRepertoires)
        int_lst_msg_id = list(map(int, lst_msg_id))
        int_lst_msg_id.sort()
        print(int_lst_msg_id)
        newer_than = int_lst_msg_id[-1]
        print(newer_than)
        flux_efc3 = yammer.messages.from_group(group_id, newer_than=newer_than)
        lst_new_msg = flux_efc3['messages']
        lst_new_msg.reverse()

        for new_msg in lst_new_msg:
            lst_msg_id.append(str(new_msg['id']))

            print(new_msg['id'])

            user = yammer.users.find(new_msg['sender_id'])
            sender = user['full_name']
            msg = new_msg['body']['parsed']

            os.mkdir('timeline/' + str(new_msg['id']))
            dirname = 'timeline/' + str(new_msg['id']) + '/'

            with open(dirname + "README.txt", "w") as file:
                file.write(msg)
                file.write("\n\n*" + sender + "*")
                file.close()

            #sdmsg(whtspp_grp, msg)
            print("Envoie msg")

            pj = []
            for attachment in new_msg['attachments']:
                pj.append(attachment['download_url'])

                flag = False
                while flag == False:

                    headers = {"Authorization": "Bearer " + access_token}
                    response = requests.get(attachment['download_url'], headers=headers)
                    print(response)

                    if response.status_code == 200:
                        with open(dirname + attachment['name'], 'wb') as f:
                            f.write(response.content)
                        print("Envoie doc")
                        print(dirname.strip(self,1),attachment['name'])
                        sdpdf(whtspp_grp, dirname, attachment['name'], dirname)
                        time.sleep(30)
                        flag = True

                    else:
                        print('Echec de téléchargement, attente de 30 secondes.')
                        time.sleep(30)
            #for name in os.listdir(dirname):
                #sdpdf(whtspp_grp,dirname,name,dirname)
            print("================================================")

    except IndexError:
        print("Pas de nouveau message !")
        print("================================================")
        time.sleep(30)

    except:
        print("Une erreur c'est produite !")
        print("================================================")
        time.sleep(60)

