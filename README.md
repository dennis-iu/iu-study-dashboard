<center>Study Dashboard</center>  
<center>DLBDSOOFPP01_D - Objektorientierte und funktionale Programmierung mit Python</center>  
<center>Portfolio - Erarbeitung</center>  

**Voraussetzungen:**  
- Python 3.x  
- pyenv  
- docker-compose  
- ggf. make  

**Einrichtung mit make:**  
 - make prepare in der Konsole ausführen
 - angezeigten Schritten folgen
   
**Einrichtung ohne make:**  
 - virtuelle Python Umgebung erzeugen:  
    pyenv virtualenv <deine-python-version> study-env  
 - virtuelle Umgebung aktivieren:  
    pyenv activate study-env  
 - Abhängigkeiten aus der requirements.txt installieren:  
    pip install -r requirements.txt  

**Ausführung des Projektes:**
 - docker-compose up -d (Danach etwa 10-30 Sekunden warten)
 - python main.py
  
**Aufbau des Projektes:**  
Weitere Doku folgt...  