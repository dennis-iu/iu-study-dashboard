<center>Study Dashboard</center>  
<center>DLBDSOOFPP01_D - Objektorientierte und funktionale Programmierung mit Python</center>  
<center>Portfolio - Erarbeitung</center>  

**Voraussetzungen erfüllen:**  
- Linux oder wsl einrichten  
- Abhängigkeiten über folgende Befehle installieren
```bash 
sudo apt update && sudo apt upgrade -y  
sudo apt install -y build-essential python3 python3-pip python3-venv git curl unzip  
sudo apt install -y docker.io docker-compose  
```
 - pyenv installieren 
 ```bash 
sudo apt update && sudo apt install -y \  
build-essential curl git libbz2-dev libreadline-dev libssl-dev \  
libsqlite3-dev zlib1g-dev libffi-dev libncursesw5-dev xz-utils tk-dev  
```
```bash
curl https://pyenv.run | bash  
```
 - nano ~/.bashrc   # oder ~/.zshrc  
 - folgendes ganz unten einfügen    
```bash
export PYENV_ROOT="$HOME/.pyenv"  
export PATH="$PYENV_ROOT/bin:$PATH"    
eval "$(pyenv init --path)"    
eval "$(pyenv init -)"    
eval "$(pyenv virtualenv-init -)"    
```
 - speichern, rausgehen und über source ~/.bashrc neu laden    
 - funktioniert pyenv --version, ist pyenv korrekt installiert  
 - gewünschte python Version installieren 
 ```bash 
pyenv install [deine-python-version>]  
```

**Weitere Einrichtung mit make:**  
 - in der Konsole ausführen (danach etwa 10-30 Sekunden warten):
 ```bash  
make prepare [deine-python-version]
pyenv activate study-env   
```

**Ausführung des Projektes:**  
```bash
python main.py  
```

**Aufbau des Projektes:**  
<div align="center">
  <img src="readme_assets/study_dashboard_uml.png" alt="study_dashboard_uml">
</div>

**Nutzung des Projektes:**  
1. Ausführen der main.py  
<div align="center">
  <img src="readme_assets/empty_homeui.png" alt="empty_homeui">
</div>

2. Über den Course Changes Button zur Auswahlseite gelangen  
<div align="center">
  <img src="readme_assets/selectui.png" alt="selectui">
</div>  

3. Über den mittleren Pfeil der Course Changes Seite zur Add Course Seite navigieren  
<div align="center">
  <img src="readme_assets/addui.png" alt="addui">
</div>

4. Über den mittleren Pfeil der Course Changes Seite zur Change Status Seite navigieren  
<div align="center">
  <img src="readme_assets/changeui.png" alt="changeui">
</div>

5. Über den rechten Pfeil der Course Changes Seite zur Delete Course Seite navigieren 
<div align="center">
  <img src="readme_assets/deleteui.png" alt="deleteui">
</div> 

6. Dropdowns verwenden  
<div align="center">
  <img src="readme_assets/ui_dropdown.png" alt="ui_dropdown">
</div> 

7. Eingabe-Ergebnisse auf der Startseite begutachten (Zurück über den Button oben links)
<div align="center">
  <img src="readme_assets/homeui.png" alt="homeui">
</div>  

8. Gegebenfalls weitere Eingaben oder Änderungen über die gezeigten Möglichkeiten vornehmen
