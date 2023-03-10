import requests
import argparse
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
try:
    version = "0.05"
    parser = argparse.ArgumentParser(description='Scraps The Lodestone For FFXIV Players.',prog="FFXIV SCRAPER")
    parser.add_argument("--version", help="prints The script version(currently on version {})".format(version), action="version", version="%(prog)s {}".format(version))
    parser.add_argument("-n", help="change the range of the for loop", nargs=2, type=int)
    parser.add_argument("-d", "--debug",help="output to file data.txt", action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose output (more v = more verbosity)", action="count")
    args = parser.parse_args()
    timeNow = time.strftime("%H:%M:%S")
    def main():
        if args.n:
            forOne = args.n[0]
            forTwo = args.n[1]
            if forOne > forTwo:
                print("N1 Must Be Lower Than N2!")
                exit()
        else:
            forOne = 1
            forTwo = 100
        pbar = tqdm(range(forOne,forTwo))
        for i in pbar:
            if args.verbose == 2:
                pbar.set_postfix_str(s="Started {}".format(timeNow))
            #tqdm.write("started at {}".format(time.strftime("%H:%M:%S")))
            URL = f'https://na.finalfantasyxiv.com/lodestone/character/{i}/'#35914598 my character
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')

            URLClass = f"https://na.finalfantasyxiv.com/lodestone/character/{i}/class_job/"
            pageClass = requests.get(URLClass)
            soupClass = BeautifulSoup(pageClass.content, 'html.parser')
            pbar.refresh()
            
            playerID = i
            if page.status_code != 404:
                title = soup.find("title").getText().split("|",1)[0]
                #ninLVL = soupClass.findAll("img", alt="", height="24") 
                #<img alt="" class="js__tooltip" data-tooltip="Ninja / Rogue" height="24" src="https://img.finalfantasyxiv.com/lds/h/0/Fso5hanZVEEAaZ7OGWJsXpf3jw.png" width="24"/>62</li>
                ninLVL = soupClass.findAll("div")
                border = "######################"
                #print(ninLVL)
                pbar.refresh()
                output = f"Status Code: {page.status_code}\nPlayer Name: {title}\nID: {playerID}\nURL: {URL}\n"
                tqdm.write(f"{border}\nStatus Code: {page.status_code}\nPlayer Name: {title}\nID: {playerID}\nURL: {URL}")
                ID = i + 1
                if page.status_code == 404:
                    ID += 1
                    pbar.refresh()
                pbar.set_description("Processing ID #%i" % ID )
                pbar.refresh()
            if args.verbose == 1 or args.verbose == 2 and page.status_code == 404:
                tqdm.write(f"#######################\nPlayer ID {playerID} Not Found!")
                pbar.refresh()
            if args.debug:
                outFile = open("data.txt", "w")
                outFile.write(str(output))
                outFile.close()
    main()
except KeyboardInterrupt:
    tqdm.write(" EXITING ")
