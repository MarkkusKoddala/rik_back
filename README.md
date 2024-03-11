Flaski Rakenduse Serveri Seadistamine
See juhend aitab teil seadistada Flaski rakenduse serveri, tõmmates koodi alla Gitist ja seadistades arenduskeskkonna.

Eeltingimused
Enne alustamist veenduge, et teie süsteemis on paigaldatud järgmised tööriistad:

Git
Python (versioon 3.6 või uuem)
pip (Pythoni paketihaldur)
1. Koodi Allalaadimine Gitist
Esmalt kloonige soovitud Flaski rakenduse repositoorium kohalikku süsteemi kasutades Git käsurida. Asendage repositooriumi-url tegeliku repositooriumi URL-iga:

bash
Copy code
git clone repositooriumi-url
See käsk laadib alla kogu repositooriumi sisu teie valitud kausta.

2. Virtuaalse Keskkonna Seadistamine
Virtuaalse keskkonna loomine on soovitatav, et hoida projektis kasutatavad sõltuvused eraldatud teistest Pythoni projektidest. Virtuaalse keskkonna loomiseks ja aktiveerimiseks kasutage järgmisi käsklusi:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # Linux või macOS
venv\Scripts\activate.bat # Windows
3. Sõltuvuste Paigaldamine
Navigeerige projekti juurkausta (kust leiate requirements.txt faili) ja käivitage järgmine käsk, et paigaldada kõik vajalikud sõltuvused:

bash
Copy code
pip install -r requirements.txt
4. Rakenduse Käivitamine
Peale sõltuvuste paigaldamist saate Flaski rakenduse käivitada järgmise käsklusega:

bash
Copy code
flask run
Või kui teie rakendus kasutab app.py või main.py faili rakenduse käivitamiseks:

bash
Copy code
python app.py
5. Rakendusele Juurdepääs
Kui rakendus on käivitatud, saate sellele juurde pääseda veebibrauseris aadressil http://localhost:5000, kui te ei ole muutnud vaikimisi seadistusi.