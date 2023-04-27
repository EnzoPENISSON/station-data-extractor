from lxml import html
import requests


class PrixStation:
    def __init__(self):
        self.prod = []
        self.carburant = []
        self.devise = ''
        self.date_mise_a_jour = ''
        self.url = ''
        self.urlWebSite = ""

    def station(self, url):
        page = requests.get(url)

        tree = html.fromstring(page.content)

        for tbl in tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_UCCarburantPDV_pnlDernierPrixTable"]/div[1]/table'):

            produit = tbl.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_UCCarburantPDV_pnlDernierPrixTable"]/div[1]/table/tbody/tr/th/text()')

            elements = tbl.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_UCCarburantPDV_pnlDernierPrixTable"]/div[1]/table/tbody/tr/td/span/text()')

            vir = tbl.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_UCCarburantPDV_pnlDernierPrixTable"]/div[1]/table/tbody/tr/td/span/span/text()')

            maj = tbl.xpath(
                '//*[@id="aspnetForm"]/div[5]/div[3]/div[1]/div[1]/div[2]/div/small/text()')

            compt = 0
            for i, j in zip(elements, range(len(elements))):
                if j % 3 == 0:
                    elements[j] += vir[compt]
                    compt += 1

            prix = []

            money = elements[1]

            for euro in elements:
                if euro == "€":
                    elements.remove(euro)

            date_maj = elements[1]

            for k in range(len(elements)):
                if k % 2 == 0:
                    prix.append(elements[k])

            self.prod = produit
            self.carburant = prix
            self.devise = money
            self.date_mise_a_jour = date_maj

            return [produit, prix, money, date_maj, maj]

    def find_url(self, departement, ville, stationservice):
        page = requests.get(self.urlWebSite + departement + "/")

        tree = html.fromstring(page.content)
        link = list(tree.iterlinks())
        lien = "/prix-carburants/" + departement + "/"
        for k in range(len(link) - 1):
            if ville in link[k][2] and stationservice in link[k][2]:
                print("https://www.carburants.org"+link[k][2])
                self.url = "https://www.carburants.org"+link[k][2]
