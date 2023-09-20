<div id="top"></div>

<!-- PROJECT SHIELDS -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/christopher-chandler/De_NP_Kongru">
     <img src="app_resources/readme/logo.png" alt="Logo" width="250" height="80">
  </a>

![Version][Version-shield]  [![MIT License][license-shield]][license-url] ![update][update-shield]

[![Stargazers][stars-shield]][stars-url]

![Windows][windows-shield] ![Mac][Mac-shield]

<h3 align="center">DeNp Kongru</h3>
  <p align="justify">
    Ein NLP-Projekt zur Bestimmung von Kongruenz in deutschen Nominalphrasen 
    in Lernertexten aus dem Lernerkorporus <a href="https://www.merlin-platform.eu/" target="_blank">Merlin</a>. 
    Dieses Projekt wurde im Rahmen des computerlinguistischen Kurses
    <code>Korpuslinguistische Analysen der Nominalflexion im Deutschen (050041-SoSe23)</code>
    an der Ruhr-Universitaet Bochum in Deutschland entwickelt.
    <br />
    <br />
    <a href="https://github.com/christopher-chandler/De_NP_Kongru/issues">Fehler melden</a>
    ·
    <a href="https://github.com/christopher-chandler/De_NP_Kongru/issues">Funktion anfragen</a>
  </code>
</div>
 
<!-- TABLE OF CONTENTS -->
<details>
    <summary>Inhaltsverzeichnis</summary>
    <ol>
        <li><a href="#ueber-das-projekt">ueber das Projekt</a></li>
        <ul>
            <li><a href="#hintergrund">Hintergrund</a></li>
            <li><a href="#ergebnisse">Ergebnisse</a></li>
        </ul>
        <li><a href="#verwendete-ressourcen">Verwendete Ressourcen</a></li>
        <ul>
            <li><a href="#libraries">Libraries</a></li>
            <li><a href="#korpora">Korpora</a></li>
            <li><a href="#zusaetzliche-tools">Zusaetzliche Tools</a></li>
        </ul>
        <li><a href="#erste-schritte">Erste Schritte</a></li>
        <ul>
            <li><a href="#korpora-entpacken">Korpora entpacken</a></li>
            <li><a href="#hauptverzeichnis-festlegen">Hauptverzeichnis festlegen</a></li>
            <li><a href="#voraussetzungen">Voraussetzungen</a></li>
            <li><a href="#installation">Installation</a></li>
        </ul>
        <li><a href="#anwendung">Anwendung</a></li>
        <ul>
            <li><a href="#api">API</a></li>
            <li><a href="#cli">CLI</a></li>
            <li><a href="#ordnerstruktur">Ordnerstruktur</a></li>
            <li><a href="#analyse-durchfuehren">Analyse durchfuehren</a></li>
            <ul>
              <li><a href="#ergebnisdatei">Ergebnisdatei</a></li>          
                <li><a href="#ergebniscodes">Ergebniscodes</a></li>    
                <li><a href="#nicht-kongruenz">Kongruenz</a></li>    
                <li><a href="#kongruenz">Nicht Kongruenz</a></li>    
          </ul>
        </ul>
        <li><a href="#roadmap">Roadmap</a></li>
        <li><a href="#beitragen">Beitragen</a></li>
        <li><a href="#lizenz">Lizenz</a></li>
        <li><a href="#kontakt">Kontakt</a></li>
        <li><a href="#danksagungen">Danksagungen</a></li>
    </ol>
</details>

<!-- ABOUT THE PROJECT -->
# ueber das Projekt

## Hintergrund
Im Rahmen dieses Projekts soll die Kongruenz in deutschen Nominalphrasen 
bestimmt werden. Daraus resultierend werden die Ergebnisse aus verscheidenen
Lernergruppen miteinander verglichen, um die Unterschiede zwischen
den jeweiligen Sprechergruppen z.B. Spanisch, Franzoesisch, Deutsch, etc
veranschaulichen zu koennen.

## Ergebnisse
ausstehend

<div align="center">
  <a href="https://github.com/christopher-chandler/De_NP_Kongru">
  </a>
</div>
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

# Verwendete Ressourcen
Eine Liste der Ressourcen, die bei der Entwicklung des Programms verwendet wurden.

## Libraries

### Pip
 - [click==8.1.3](https://pypi.org/project/click/8.1.3/)
- [pandas==1.5.2](https://pypi.org/project/pandas/1.5.2/)
- [PyYAML==6.0.1](https://pypi.org/project/PyYAML/6.0.1/)
- [rich~=12.6.0](https://pypi.org/project/rich/12.6.0/)
- [scikit_learn==1.1.3](https://pypi.org/project/scikit-learn/1.1.3/)
- [textdistance==4.5.0](https://pypi.org/project/textdistance/4.5.0/)
- [tqdm==4.64.1](https://pypi.org/project/tqdm/4.64.1/)
- [typer~=0.4.2](https://pypi.org/project/typer/0.4.2/)

### Korpora 

* [MERLIN Corpus](https://www.merlin-platform.eu/)
* [Deutsche morphologische Woerterbuecher](https://github.com/DuyguA/german-morph-dictionaries)

### Zusaetzliche Tools
 Diese Tools wurden benutzt, um die Lernertexte zu taggen und zu parsen.
Dieses Verfahren wurde in einem anderen, verwandten [Projekt](https://github.com/imgeyuez/automatic_np_extraction) gemacht.
* [Parzu - deutscher Parser](https://github.com/rsennrich/ParZu)
* [Conluu - CoNLL-U Parser](https://pypi.org/project/conllu/)
  *  Wie genau diese Tools verwendet wurden, bitte [hier nachlesen](https://github.com/imgeyuez/automatic_np_extraction)

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- GETTING STARTED -->
# Erste Schritte

### Korpora entpacken
 Das Projekt bezieht sich auf einige Korpora und Datenbanken. Ohne diese kann das 
Projekt nicht gestartet werden. 

Alle korpora muessen erstmal entpackt werden: 

app_resources/data/demorphy
- [demorphy_de_kongru.zip](app_resources%2Fdata%2Fdemorphy%2Fdemorphy_de_kongru.zip)

app_resources/data/merlin_corpus
- [merlin_corpus.db.zip](app_resources%2Fdata%2Fmerlin_corpus%2Fmerlin_corpus.db.zip)

Die Verzeichnisse sollte nachher die folgenden Strukturen haben: 

Demorphy
- Inhalt 
  - [demoprhy_dict.pkl](app_resources%2Fdata%2Fdemorphy%2Fdemoprhy_dict.pkl)
  - [demorpy_dict.txt](app_resources%2Fdata%2Fdemorphy%2Fdemorpy_dict.txt)

Merlin

- Inhalt
  - [merlin_corpus.db.zip](app_resources%2Fdata%2Fmerlin_corpus%2Fmerlin_corpus.db.zip)
  - [merlin_raw_corpus.zip](app_resources%2Fdata%2Fmerlin_corpus%2Fmerlin_raw_corpus.zip)
    - Das sind die Datein, womit die SQL-DB erzeugt wurde. Diese muss man nur entpacken
    - wenn man eine neue SQL-DB erstellen moechte.
  - [CHANGELOG.md](app_resources%2Fdata%2Fmerlin_corpus%2FCHANGELOG.md)
  - [README.md](app_resources%2Fdata%2Fmerlin_corpus%2FREADME.md)
  - [merlin_corpus.db](app_resources%2Fdata%2Fmerlin_corpus%2Fmerlin_corpus.db)

Andere Korpora und Dateien sind zwar enthalten, aber diese muessen nicht 
entpackt werden. 
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

### Hauptverzeichnis festlegen
Als naechstes muss das Hauptverzeichnes des Projekts festgelegt werden. 
Dies tut man in der `main_config.yaml` Datei.
z.B. 
- `/Users/christopherchandler/de_np_kongru`

# Voraussetzungen
 Das Programm wurde mit [Python 3.10](https://www.python.org/downloads/release/python-3100/) konzepiert und entwicklet. 
 Es besteht die Moeglichkeit  eine altere Python-Version zu benutzen, aber dann kann es
sein, dass das Programm nicht stabil ist. 
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

# Installation
Um die notwendige libraries installieren zu koennen, das folgendene Kommando
in der Konsole ausgeben: `pip install -r requirements.txt` 

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- USAGE EXAMPLES -->
## Anwendung 

### API
Wenn man die Module einfach so importieren will, 
kann man das auch ueber den ganz normalen Weg machen. 

```
from kongru.api_nlp.congruential_analysis.app_congruential_analysis import (
 nominal_phrase_agreement_analysis ) 
```
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

### CLI

Um DeNP Kongru als CLI starten zu koennen,  den `python main.py` im Hauptverzeichnis
ausfuehren. Wenn alles korrekt eingerichtet wurden, soll Folgendes in der Konsole 
erscheinen

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Die Hauptapp von DeNpKongru

Commands:
  datenbank           Die Datenbankcorpora verwalten und durchsuchen
  kongruenz           Die Np-Eintraege auswerten
  statistik           Eine einfache Analyse ueber DeNpKongru ausfuehren
  verzeichnis_leeren  Ein ausgewaehltes Verzeichnis leeren
christopherchandler@Mac-Studio de_np_kongru % 
```

Bei jedem Befehl kann man einen Hinweis ausgeben lassen, wie die Befehle funktionieren
und welche Argumente erforderlich sind, indem man `--help` am Ende eingibt.  

Zum Beispiel: 
 
`python main.py datenbank text_lesen --help`

```
Usage: main.py datenbank text_lesen [OPTIONS]

  einen bestimmten Text in der Datenbank lesen

Options:
  --text_id, --id TEXT  Die Text-Id des gewuenschten Textes angeben  [default:
                        1031_0003130]
  --help                Show this message and exit.
```

Um genauer zu wissen, wie diese Schnittstelle funktioniert oder Fehlermeldung besser zu
verstehen, bitte die Dokumentation von [Typer](https://typer.tiangolo.com/) durchlesen.
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

### Ordnerstruktur
Die Dateien, die DeNpKongru braucht, um eine Analyse durchzufuehren. 
Die Order sind zwar leer, aber werden befuellt, je nachdem welche Kommandos 
man ausfuehlt. Man kann auch die Dateien manuell in dem entsprechenden Ordner 
ablegen.

- [user](user)
  - Die dateien, die vom Benutzer abgelegt, generiert oder benutzt wird. 
    - [incoming](user%2Fincoming)
      - [ast](user%2Fincoming%2Fast)
        - Die Conll-Datei als Python Listen 
      - [conll](user%2Fincoming%2Fconll)
        - Die Conll-Dateien
      - [full_json](user%2Fincoming%2Ffull_json)
        - Die Merlin-Texte als Json-Dateien
      - [pylist](user%2Fincoming%2Fpylist)
        - Das Gleiche wie die AST-Dateien, aber die interne Struktur ist eine andere. 
      - [raw](user%2Fincoming%2Fraw)
        - Die einfachen Merlin-Texte
    - [kongru_evaluation](user%2Fkongru_evaluation)
      - Die Dateien, um das Programm auszuwerten, werden hier gespeichert 
        - [gold_files](user%2Fkongru_evaluation%2Fgold_files)
          - alle korrigierter NP-Dateien muessen in diesem Verzeichnis liegen
        - [raw_files](user%2Fkongru_evaluation%2Fraw_files)
          - die entsprechenden unkorrigierten Dateien muessen auch in diesem Verzeichnis liegen.
            Sie werden miteinander verglichen, um *precision*, *recall* und *f1-score* zu generieren.
  - [outgoing](user%2Foutgoing) <br>
      Hier werden die Ergebnisse gespeichert. 
<br>
    - [batch_results](user%2Foutgoing%2Fbatch_results)  
      - wenn man [main_np_analysis.py](main_np_analysis.py) ausfuehrt, 
      werden die Ergebnisse hier als .csv-Datei gespeichert. 
    - [extracted_nominal_phrases](user%2Foutgoing%2Fextracted_nominal_phrases)
      - Die unverarbeiteten Nominalphrasen, die aus den AST oder Pylist-dateien 
        extrahiert wurden, werden hier gespeichert.
      
    - [nominal_phrase_analysis_results](user%2Foutgoing%2Fnominal_phrase_analysis_results)
      - Die Auswertung der Nominalphrasen werden hier gespeichert. 
    - [nominal_phrase_json](user%2Foutgoing%2Fnominal_phrase_json)
      - Die Nominalphrasen und deren Ergebnisse werden in der entsprechenden JSON-Datei
        gespeichert. 
    - [text_ids](user%2Ftext_ids)
      - Dieser Ordner enthaelt die Dateien `test_ids.txt` und `training_ids.txt`. 
      Die sind wichtig fuer [main_np_analysis.py](main_np_analysis.py). Alle Ids,
      sofern sie in der SQL-DB existieren, werden eingelesen und ausgewertet. 
      - 
 <p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>


### Analyse durchfuehren
Die Analyse kann man entweder ueber die API oder die CLI durchfuehren. 
Ein vorgefertiges Skript - [main_np_analysis.py](main_np_analysis.py) - um dies zu tun
findet man im Hauptverzeichnis. Daran kann man sich orientieren, wenn man neue 
Skript anlegen moechte.
Wenn die Pfade korrekt eingerichtet wurden, 
sollte dieses Skript problemlos funktioniern.
Man muss also nur das Skript starten. 

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

#### Ergebnisdatei
Das Programm erwartet die folgende Struktur:

``` 
CSV
Nominalphrase,Morphologische Information, Satz  

Maria Schmidt,Maria N Masc|_|Sg,Schmidt N Masc|_|Sg,Maria Schmidt Addresse Computer Spezialist Odenwaldstraße 5.
```

Alle Ergebnisse Dateien haben die folgene Struktur: 

```
CSV
Ergebniscode, Nominalphrase, Morphologische Information, Satz
1,Maria Schmidt,"Maria,N,_|Masc|_|Sg","Schmidt,N,_|Masc|_|Sg",Maria Schmidt Addresse Computer Spezialist Odenwaldstraße 5.
```

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

### Ergebniscodes 
Es werden hier verschiedene Kongruenzcodes aufgelistet, um festzustellen,
um welche Art von Kongruenz es sich handelt.

| Arten            | Beispiel                             |
|------------------|--------------------------------------|
| EINFACH          | Stadt                                |
| ART              | Das Leben                            |
| PREP             | Mit Kindern                          |
| Rechtschreibfehler | Reche Pfliche*,Wiviel*               |
| Eigennamen       | Katharina, Maria Meier               |
| Redewendungen    | Liebe Julia, Mit freundlichen Grüßen |

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

##### Kongruenz
Gruende, weswegen die Nominalphrase kongruiert

| Code | Bedeutung                      |
|------|--------------------------------|
| 0    | EINFACH                        |
| 1    | ART                            |
| 2    | PREP                           |
| 3    | Eigennamen                     |
| 4    | Redewendung bzw. gaengiger Satz |

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

##### Nicht Kongruenz
Gruende, weswegen die Nominalphrase nicht kongruiert

| Code | Bedeutung     |
|------|-------------|
| 10   | EINFACH     |
| 11   | ART         |
| 12   | PREP        |
| 99   | Unbekannt   |

- 99 - Aus unbekannten Gruenden konnte die Kongruenz nicht bestimmt werden.
Es ist vermutlich irgendwo ein Fehler aufgetreten. Es kann auch sein,
dass die Kongruenz einfach nicht ermittelt werden konnte.

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- ROADMAP -->
# Roadmap

Siehe die [offenen Probleme](https://github.com/christopher-chandler/De_NP_Kongru/issues) fuer eine vollstaendige Liste der vorgeschlagenen Funktionen (und bekannten Probleme).

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- CONTRIBUTING -->
# Beitragen
Beitraege sind es, die die Open-Source-Community zu einem erstaunlichen Ort zum 
Lernen, Inspirieren und Erschaffen machen.
Jegliche Beitraege, die Sie leisten, werden **sehr geschaetzt**.

Wenn Sie eine Idee haben, die dieses Projekt verbessern wuerde, bitte machen 
Sie einen Fork des Repositories und erstellen Sie einen Pull Request.
Sie koennen auch einfach ein Problem mit dem Tag "Verbesserung" eroeffnen.
Vergessen Sie nicht, dem Projekt einen Stern zu geben! Vielen Dank nochmals!

1. Forken Sie das Projekt.
2. Erstellen Sie Ihren Feature-Branch (`git checkout -b feature/ErstaunlicheFunktion`).
3. Machen Sie Ihre aenderungen (`git commit -m 'Fuege einige erstaunliche Funktionen hinzu'`).
4. Pushen Sie den Branch (`git push origin feature/ErstaunlicheFunktion`).
5. Eroeffnen Sie einen Pull Request.

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>


<!-- LICENSE -->
# Lizenz
Vertrieben unter der MIT-Lizenz. Siehe `LIZENZ` fuer weitere Informationen.

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- CONTACT -->
# Kontakt
Christopher Chandler - christopher.chandler at outlook.de
* Project Link: [De_NP_Kongru](https://github.com/christopher-chandler/De_NP_Kongru)
<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>

<!-- ACKNOWLEDGMENTS -->
# Danksagungen

* [Imge Yuezuencueoglu](https://github.com/imgeyuez)
* [Georg Stin]()
* [Ikram Abdalla]()

<p align="right">(<a href="#top">Zurueck zum Anfang</a>)</p>
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/christopher-chandler/De_NP_Kongru?color=green&logoColor=%20
[contributors-url]: https://github.com/christopher-chandler/De_NP_Kongru/graphs/contributors

[stars-shield]: https://img.shields.io/github/stars/christopher-chandler/De_NP_Kongru?logoColor=yellow&style=social
[stars-url]: https://github.com/christopher-chandler/De_NP_Kongru/stargazers

[license-shield]: https://img.shields.io/github/license/christopher-chandler/De_NP_Kongru?color=yellow
[license-url]: https://github.com/christopher-chandler/De_NP_Kongru/blob/master/LICENSE.txt

[download-shield]: https://img.shields.io/github/downloads/christopher-chandler/De_NP_Kongru/total

[windows-shield]:  https://img.shields.io/badge/Windows-Tested-purple 
[mac-shield]: https://img.shields.io/badge/Mac-Tested-purple
[version-shield]: https://img.shields.io/badge/Version-0.0.1-brightgreen
[update-shield]: https://img.shields.io/badge/Last_Updated-08_2023-blue
 
