import os
import discord
from discord.ext import tasks
import requests
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
apiKey = os.getenv("APIKEY")
assetList = []
best5 = []
watchList = []
actualWatch = "ETH"

client = discord.Client()

async def changeDiscordStatus(crypto):
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{crypto['asset_id']} {formatNumber(crypto['price_usd'])}$"
        )
    )

def hasUSD(crypto):
    if "price_usd" in crypto.keys():
        return True

def isCryptoIn(str):
    for crypto in assetList:
        if crypto['asset_id'].lower() == str.lower():
            return True
    for crypto in assetList:
        if crypto['name'].lower() == str.lower():
            return True
    return False

def getCryptoId(str):
    for id, crypto in enumerate(assetList):
        if crypto['asset_id'].lower() == str.lower():
            return id
    for id, crypto in enumerate(assetList):
        if crypto['name'].lower() == str.lower():
            return id
    return 0

def getCryptoById(id):
    return assetList[id]

def formatNumber(nbr):
    varRet = float('{:.2f}'.format(nbr))
    return("{:,}".format(varRet))

def cryptoUsdDayVolume(crypto):
    if 'type_is_crypto' in crypto.keys():
        if 'volume_1day_usd' in crypto.keys() and crypto['type_is_crypto'] == 1:
            return crypto['volume_1day_usd']
    return 0

def get5BestCryptos():
    actuAssets()
    global best5
    best5 = sorted(assetList, key=lambda dic: cryptoUsdDayVolume(dic), reverse=True)[0:5]

def actuAssets():
    f=open("assets.json", "r")
    global assetList
    assetList = json.loads(f.read())

@client.event
async def on_ready():
    print("le bot '{0.user}' est prêt.".format(client))
    assetRequest.start()

# on raffraichit la liste des assets toutes les 15 minutes (je peux pas faire moins à cause de la clé de l'api gratuite qui me limite à 100 requetes/jour)
@tasks.loop(minutes=15)
async def assetRequest():
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key' : apiKey}
    response = requests.get(url, headers=headers)
    f = open("assets.json", "w")
    f.write(response.text)
    f.close()
    crypto = getCryptoById(getCryptoId(actualWatch))
    await changeDiscordStatus(crypto)
    actuAssets()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    messageText = message.content
    
    # Pour tester si le bot reçoit bien les messages et peut y répondre
    if messageText.lower().startswith("$test") :
        await message.channel.send("ça marche bien !", delete_after=10)
        
    # Message d'aide
    if messageText.lower().startswith("$help") :
        await message.channel.send(""":book: 
$help pour avoir de l'aide
$test pour tester si le bot peut bien envoyer un message dans le channel
$info <Monnaie> pour obtenir des infos sur une monnaie
$delete <nombre> supprime le nombre de messages demandé
$status <Monnaie> change le statut du bot discord afin qu'il indique une autre crypto
$best affiche les 5 cryptomonnaies qui ont le plus été échangées dans la journée
                                   """)
        
    # récupérer les informations d'une monnaie    
    if messageText.lower().startswith("$info"):
        cryptoCode = messageText.split()[1]
        if isCryptoIn(cryptoCode):
            crypto = getCryptoById(getCryptoId(cryptoCode))
            await message.channel.send(f":money_with_wings:\nInformations sur : {crypto['name']} ou {crypto['asset_id']}\nValeur en USD: {formatNumber(crypto['price_usd'])} $\nQuantité échangée aujourd'hui: {formatNumber(crypto['volume_1day_usd'])} $\nPremière entrée: {crypto['data_start']}\nDernière entrée: {crypto['data_end']}")
            
            
    # Supprimer un certain nombre de messages d'un s
    if messageText.lower().startswith("$delete"):
        nbr = int(message.content.split()[1])
        messageList = await message.channel.history(limit=nbr+1).flatten()
        
        for delMessage in messageList:
            await delMessage.delete()

    # changer la crypto d'affichage du statut du bot
    if messageText.lower().startswith("$status"):
        cryptoCode = messageText.split()[1]
        if isCryptoIn(cryptoCode):
            crypto = getCryptoById(getCryptoId(cryptoCode))
            if hasUSD(crypto):
                global actualWatch
                actualWatch = cryptoCode
                await changeDiscordStatus(crypto)
                await message.channel.send(f":white_check_mark: Affichage changé ! ")
            else:
                await message.channel.send(f":no_entry_sign: Cette monnaie n'a pas d'équivalent en USD ! ")
        else:
            await message.channel.send(f":no_entry_sign: Nous n'avons pas trouvé la monnaie dont tu parles ! ")
    
    # top 5 des cryptos les plus échangées dans la journée
    if messageText.lower().startswith("$best"):
        get5BestCryptos()
        await message.channel.send(f"""
Voici les 5 Cryptomonnaies les plus échangées dans les dernières 24H :moneybag:
        ```
n°1 {best5[0]['name']} aka {best5[0]['asset_id']}
Valeur actuelle en USD: {formatNumber(best5[0]['price_usd'])}
Quantité échangée aujourd'hui: {formatNumber(best5[0]['volume_1day_usd'])} USD

n°2 {best5[1]['name']} aka {best5[1]['asset_id']}
Valeur actuelle en USD: {formatNumber(best5[1]['price_usd'])}
Quantité échangée aujourd'hui: {formatNumber(best5[1]['volume_1day_usd'])} USD

n°3 {best5[2]['name']} aka {best5[2]['asset_id']}
Valeur actuelle en USD: {formatNumber(best5[2]['price_usd'])}
Quantité échangée aujourd'hui: {formatNumber(best5[2]['volume_1day_usd'])} USD

n°4 {best5[3]['name']} aka {best5[3]['asset_id']}
Valeur actuelle en USD: {formatNumber(best5[3]['price_usd'])}
Quantité échangée aujourd'hui: {formatNumber(best5[3]['volume_1day_usd'])} USD

n°5 {best5[4]['name']} aka {best5[4]['asset_id']}
Valeur actuelle en USD: {formatNumber(best5[4]['price_usd'])}
Quantité échangée aujourd'hui: {formatNumber(best5[4]['volume_1day_usd'])} USD
        ```
        """)
    

actuAssets()

client.run(token)