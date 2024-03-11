
# RIK server

See juhend aitab teil seadistada Flaski rakenduse serveri, tõmmates koodi alla Gitist ja seadistades arenduskeskkonna.

## Eeltingimused

Enne alustamist veenduge, et teie süsteemis on paigaldatud järgmised tööriistad:

- Git
- Python (versioon 3.6 või uuem)
- pip (Pythoni paketihaldur)

## Koodi Allalaadimine Gitist

Esmalt kloonige soovitud Flaski rakenduse repositoorium kohalikku süsteemi kasutades Git käsurida. 

```bash
git clone https://github.com/MarkkusKoddala/rik_back.git
```

See käsk laadib alla kogu repositooriumi sisu teie valitud kausta.

## Mine projekti kausta
```bash cd rik_back```


## Virtuaalse Keskkonna Seadistamine

Virtuaalse keskkonna loomine on soovitatav, et hoida projektis kasutatavad sõltuvused eraldatud teistest Pythoni projektidest. Virtuaalse keskkonna loomiseks ja aktiveerimiseks kasutage järgmisi käsklusi:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux või macOS
venv\Scripts\activate.bat  # Windows
```

## Sõltuvuste Paigaldamine

Navigeerige projekti juurkausta (kust leiate `requirements.txt` faili) ja käivitage järgmine käsk, et paigaldada kõik vajalikud sõltuvused:

```bash
pip install -r requirements.txt
```

## Rakenduse Käivitamine

Peale sõltuvuste paigaldamist saate Flaski rakenduse käivitada järgmise käsklusega:

```bash
python app.py
```

## Rakendusele Juurdepääs

Kui rakendus on käivitatud, saate sellele juurde pääseda veebibrauseris aadressil http://localhost:5000, kui te ei ole muutnud vaikimisi seadistusi.
