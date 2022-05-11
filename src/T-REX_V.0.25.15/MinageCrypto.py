from colorama import Fore
import time, os, random, sys

def Main():
  # Définition des variables nécessaires
  confirm_pool = 'non'
  confirm_wallet = 'non'
  confirm_crypto = 'non'
  crypto_choice = False
  crypto = ['ethash','kawpow','autolykos2']
  crypto_names = ['Ethereum','Ravencoin','ERGO']
  user_enters = False
  final_choice = 0
  text = """

  __  __ _                           ____                  _        
  |  \/  (_)_ __   __ _  __ _  ___   / ___|_ __ _   _ _ __ | |_ ___  
  | |\/| | | '_ \ / _` |/ _` |/ _ \ | |   | '__| | | | '_ \| __/ _ \ 
  | |  | | | | | | (_| | (_| |  __/ | |___| |  | |_| | |_) | || (_) |
  |_|  |_|_|_| |_|\__,_|\__, |\___|  \____|_|   \__, | .__/ \__\___/ 
                        |___/                   |___/|_|      
                              
  """


  # Fonction pour clear le terminal
  def Clear(crypto=False, pool=False,wallet=False):
    os.system('cls')
    if crypto:
      print (f'Crypto: {crypto}\n')
    if pool:
      print (f'Pool: {pool}')
    if wallet:
      print (f'Wallet: {wallet}')
  Clear()
  while (user_enters == False):
    colors = list(vars(Fore).values())
    colored_lines = [random.choice(colors) + line for line in text.split('\n')]
    print('\n'.join(colored_lines))
    user_enters = input('Entrer pour continuer...')
    time.sleep(0.2), Clear()
    print(Fore.WHITE+'.')

  while (confirm_crypto == 'non'):
    try :
      while (crypto_choice < 1  or crypto_choice > 3):
        Clear()
        print ('Liste de Crypto minables:\n1 - Ethereum\n2 - Ravencoin\n3 - ERGO')
        crypto_choice = int(input("Veuillez saisir votre crypto \n"))
    except TypeError:
      print ('Veuillez renseigner une valeur comprise entre 1 et 3 inclus.')
    crypto_choice -=1
    confirm_crypto = input(Fore.GREEN + f'Crypto sélectionnée: {crypto_names[crypto_choice]} . Souhaitez-vous conserver cette crypto ?' + Fore.WHITE)
      
  while (confirm_pool == 'non'):
    Clear(crypto_names[crypto_choice], False, False)
    pool = input("veuillez saisir votre pool \n")
    confirm_pool = input(Fore.GREEN + f'Pool sélectionné: {pool} . Souhaitez-vous conserver ce pool ?' + Fore.WHITE)
    if (confirm_pool == 'non'):
      pool = input("veuillez saisir votre pool \n ")

  while (confirm_wallet == 'non'):
    Clear(crypto_names[crypto_choice], pool, False)
    wallet= input("veuillez saisir l'adresse de votre wallet \n")
    confirm_wallet = input(Fore.GREEN + f'Wallet sélectionné: {wallet} . Souhaitez-vous conserver ce wallet ?' + Fore.WHITE)
    if (confirm_wallet == 'non'):
      wallet = input("Veuillez saisir l'adresse de votre wallet : \n")

  Clear()
  print (Fore.GREEN+f'/!\ Crypto: {crypto_names[crypto_choice]}\nPool: {pool}\nWallet: {wallet}\n\n'+Fore.RED+'NE PAS APPUYER SUR ENTREE\n'+Fore.WHITE)
  time.sleep(5)
  while (final_choice != 1 or final_choice != 2) :
    final_choice = int(input("Souhaitez-vous valider vos choix ?\n\n1 - Oui\n\n 2 - Non\n\n"))
    if (final_choice == 1):
      print (Fore.GREEN+f'Configuration terminée. Vos choix ont bien été pris en compte.\nVeuillez patienter 5 secondes. \nMerci '+Fore.WHITE)
      time.sleep(5)
      break
    if (final_choice == 2) :
      print('Restarting...')
      Main()
      exit()

  file = open("Config.bat", "w")
  file_new_content = f't-rex.exe -a {crypto[crypto_choice]} -o {pool} -u {wallet} -p x -w rig0\npause'
  file.write(file_new_content)
  file.close()
  
Main()