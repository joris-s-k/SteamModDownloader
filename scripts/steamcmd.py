import scripts.config as conf
import os
from re import sub
import wget
import subprocess
import shutil
import json

# Variables
steamCmdLinuxUrl="https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
steamCmdWindowsUrl="https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
steamCmdPath="./scripts/steamcmd/"
workDirectory=os.getcwd()+'/scripts/steamcmd/workshop'
conDir=workDirectory+'/steamapps/workshop/content/'
def anonCheck():
    if conf.fetchConfiguration("anonymousMode") == "false":
        return conf.fetchConfiguration("steamAccountName") + " " + conf.fetchConfiguration("steamPassword")
    else:
        return "anonymous"
def checkAndDownloadSteamCmd():
    if not os.path.exists(steamCmdPath):
        os.mkdir(steamCmdPath)
    print("SteamCMD not present, Downloading...")
    if len(os.listdir(steamCmdPath)) == 0:
        if os.name == 'posix':
            wget.download(steamCmdLinuxUrl,steamCmdPath)
            shutil.unpack_archive(steamCmdPath+'steamcmd_linux.tar.gz',steamCmdPath)
            os.environ["steamCmdExe"] = "steamcmd.sh"
            os.remove(steamCmdPath+'steamcmd_linux.tar.gz')
        if os.name == 'nt':
            wget.download(steamCmdWindowsUrl,steamCmdPath)
            shutil.unpack_archive(steamCmdPath+'steamcmd.zip',steamCmdPath)
            os.environ["steamCmdExe"] = "steamcmd.exe"
            os.remove(steamCmdPath+"steamcmd.zip")
        os.mkdir('./scripts/steamcmd/workshop')
    else:
        return
def download(id,gameId,name,insDir):
    print('Downloading '+ name+'(MODID: '+id+' GAMEID: '+gameId+')')
    print('--------------------------------------------------')
    subprocess.run([steamCmdPath+os.environ["steamCmdExe"],'+force_install_dir '+workDirectory,f'+login {anonCheck()}',f'+workshop_download_item {gameId} {id}','+exit'])
    print('\n--------------------------------------------------')
    print('Moving and Renaming ' +name+' ('+id+')')
    modFol=conDir+gameId+'/'+id+'/'
    outPathName=insDir+'/'+name
    if os.path.exists(outPathName): print('Updating File (Existing File)')
    # Prepare info.json for mod
    with open(os.path.join(modFol,'smbinfo.json'), 'w') as jsonFile:
        infoData= {
            "name": name,
            "gameID": gameId
        }
        json.dump(infoData,jsonFile,indent=4)
    shutil.copytree(modFol,outPathName,dirs_exist_ok=True)
    shutil.rmtree(modFol)
