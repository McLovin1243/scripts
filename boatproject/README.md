# **Båtdeteksjon med Kunstig Intelligens**
Vi benytter bacheloren til videre utforskning av KI gjennom et prosjekt som omhandler båtdeteksjon.

Dette prosjektet bruker NVIDIA Jetson Orin Nano til å kjøre en KI-modell trent opp til å kjenne igjen båter. Man kan bruke et standardbibliotek (ssd-mobilenet-v2 fra detectNet), eller så kan man trene opp en egen modell. Jetson Orin Nano sender signaler via Ethernet til en PC, som igjen sender signaler til en PLS for lysstyring (TIA-portal, SCL). Målet vårt har vært å overvåke båter som legger til kai, logge dem, og rapportere hvor lenge de har vært fortøyd.
Prosjektet er basert på dusty-nv sin guide for å iverksette objektdeteksjon ved hjelp av detectNet: https://github.com/dusty-nv/jetson-inference

## **Struktur**

    JustServerGUI.py: script for å kun starte server
    boat_serverGUI.py: script for å starte server og oversikt over brygge
    boat_client.py: script for å kjøre video med bildedeteksjon

## **Forutsetninger for å kjøre programmet:**

- Bildegjenkjenningen er kunstig intelligens som kun kan kjøres på Nvidia.
- Installer nødvendig programvare: jetson-inference, jetson-utils, python-snap7, tkinter
- Parkeringsplasser til båtene skal legges inn på forhånd i 'boat_serverGUI.py'
- PLS-kode for lysstyring er ikke vedlagt. Den må lages.


## **Kjøring av program**

Merk hvilken mappe scriptene legges i. Begge programmene skal kjøres samtidig.

Terminal 1. Start GUI for serveren og oversikt:

    cd "mappenavn"
    python3 boat_serverGUI.py

Terminal 2. Kjør bilde- og objektgjenkjenningsskriptet:

    cd jetson-inference
    // her kjører vi docker
    cd "mappenavn"
    python3 boat_client.py

## **Drøfting**

Vi benyttet 26000 bilder i vår egentrente modell. Bildedeteksjonene fungerer foreløpig ikke bra nok. Dersom en båt legger inn til kai, vil den ofte miste båten ettersom baugen forsvinner. Ved seilbåter inkluderes ofte seilene. De store deteksjonene kan være vanskelig å jobbe med.
