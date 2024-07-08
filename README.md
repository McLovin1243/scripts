**Båtdeteksjon med Kunstig Intelligens**

Dette prosjektet bruker NVIDIA Jetson Orin Nano til å kjøre en KI-modell trent opp til å kjenne igjen båter. Modellen er trent på et datasett med 26,000 bilder. I tillegg benytter vi et standardbibliotek fra NVIDIA for å detektere flere ulike objekter. Jetson Orin Nano sender signaler via Ethernet til en PC, som igjen sender signaler til en PLS for lysstyring (TIA-portal, SCL). Målet vårt har vært å overvåke båter som legger til kai, logge dem, og rapportere hvor lenge de har vært fortøyd.
Prosjektet er basert på dusty-nv sin guide for å iverksette objektdeteksjon vha detectNet: https://github.com/dusty-nv/jetson-inference

**Struktur**

    'serverGUI_copy.py': Skript for å starte server
    'final.py': script for å runne video med bildedeteksjon

**Forutsetninger for å kjøre programmet:**

- Bildegjenkjenningen er kunstig intelligens som kun kan kjøres på Nvidia.
- Installer nødvendig programvare: jetson-inference, jetson-utils, python-snap7, tkinter
- Parkeringsplasser til båtene skal legges inn på forhånd i 'final.py'
- PLS-kode er ikke vedlagt.


**Bruk**

Merk hvilken mappe scriptene legges i. Begge programmene skal kjøres samtidig.
Terminal 1. Start GUI for serveren:

    python3 serverGUI_copy.py

Terminal 2. Kjør bilde- og objektgjenkjenningsskriptet:

    python3 final.py

**Drøfting**

Bildedeteksjonene fungerer foreløpig ikke bra nok. Dersom en båt legger inn til kai, vil den ofte miste båten ettersom baugen forsvinner.
