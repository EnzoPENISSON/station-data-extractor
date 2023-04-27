from lxml import html
import requests


def get_txt_departement(urlWebSite):
    """
        Method to fill the file departement.txt with all the departement in France
    """
    page = requests.get(urlWebSite)

    tree = html.fromstring(page.content)

    with open("departement.txt", "w") as file:
        link = list(tree.iterlinks())

        lien = "/prix-carburants/"
        for k in range(len(link) - 1):
            if lien in link[k][2] and lien != link[k][2] and link[k][2] != urlWebSite and link[k][2] != "/prix-carburants/ville/":
                dep = link[k][2].split("/")
                file.write(str(dep[2])+"\n")


def get_liste_departement():
    liste_dep = []
    file = open('departement.txt', "r")
    lines = file.readlines()
    file.close()
    # browse the file line by line
    for line in lines:
        liste_dep.append(line.strip())
    return liste_dep


def get_txt_station_par_departement(departement, fichierFinalName):
    page = requests.get(
        "https://www.carburants.org/prix-carburants/" + departement + "/")

    tree = html.fromstring(page.content)

    link = list(tree.iterlinks())

    lien = "/prix-carburants/" + departement + "/"

    with open(fichierFinalName, "a") as file:
        for k in range(len(link) - 1):
            if "i/stations/" in link[k][2]:
                logo = "https://www.carburants.org" + link[k][2]
            if lien in link[k][2] and lien != link[k][2] and link[k][
                    2] != "https://www.carburants.org/prix-carburants/" + departement + "/":
                stat = link[k][2].split("/")
                ville = stat[3].split(".")[0]
                vilien = stat[3]

                if ville == "?p=2":
                    page = requests.get(
                        "https://www.carburants.org/prix-carburants/" + departement + "/?p=2")
                    tree = html.fromstring(page.content)
                    link = list(tree.iterlinks())

                    lien = "/prix-carburants/" + departement + "/"
                    for k in range(len(link) - 1):
                        if lien in link[k][2] and lien != link[k][2] and link[k][
                            2] != "https://www.carburants.org/prix-carburants/" + departement + "/" and "?p=2" not in \
                                link[k][2]:
                            stat = link[k][2].split("/")
                            ville = stat[3].split(".")[0]
                            vilien = stat[3]
                            # print("{ 'value':'" + departement + "/" + vilien + "/" + stat[4] + "'," + "'label':'"+departement.split(".")[1]+ " - " + ville + "'," + "'subtitle':'" + stat[4].split(".")[0].lstrip() + "'," + "'urllogo':'" + logo + "',},")
                            file.write("{ 'value':'" + departement + "/" + vilien + "/" + stat[4] + "'," + "'label':'" + departement.split(".")[
                                       1] + " - " + ville + "'," + "'subtitle':'" + stat[4].split(".")[0].lstrip() + "'," + "'urllogo':'" + logo + "',}," + "\n")
                    break
                else:
                    file.write("{ 'value':'" + departement + "/" + vilien + "/" + stat[4] + "'," + "'label':'" + departement.split(".")[
                               1] + " - " + ville + "'," + "'subtitle':'" + stat[4].split(".")[0].lstrip() + "'," + "'urllogo':'" + logo + "',}," + "\n")
                    # print("{ 'value':'" + departement + "/" + vilien + "/" + stat[4] + "'," + "'label':'" +departement.split(".")[1]+ " - "+ ville + "'," + "'subtitle':'" + stat[4].split(".")[0].lstrip() + "'," + "'urllogo':'" + logo + "',},")
