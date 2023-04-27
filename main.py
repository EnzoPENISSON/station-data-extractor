from lxml import html
from tqdm import tqdm
from station import PrixStation
from fetch import get_txt_departement, get_liste_departement, get_txt_station_par_departement

currentFolder = 'departement/'
urlWebSite = "https://www.carburants.org/prix-carburants/"
fichierFinalName = "stations.dart"


def main():
    get_txt_departement(urlWebSite)  # get all the departement in a txt file
    # read all the lines in the file and saves them in a list
    lines = get_liste_departement()

    with open(fichierFinalName, "w") as file:
        file.write("final List<Map<String, dynamic>> items = [\n")

    file.close()

    print("Start...")
    # iterate over the list of departement
    for line in tqdm(lines, desc="Loading…",
                     ascii=False, ncols=75):
        # get all the station in a departement
        get_txt_station_par_departement(line.strip(), fichierFinalName)
    print("Complete.")

    with open(fichierFinalName, "a") as file:
        file.write("];\n")

    file.close()

    station = PrixStation()
    station.urlWebSite = urlWebSite

    # Try to get the price of a station
    print("--------------------------")
    print("Test gaz station :")
    print(station.station(
        "https://www.carburants.org/prix-carburants/aisne.02/bruyeres-et-montberault.kwTwT7/total_garage-petetin.qBAzEj"))


if __name__ == '__main__':
    main()
