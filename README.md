# Programme de gestion de tournoi d'échecs 

## Description
Ce programme, nommé  Chess Tournament Manager, a été conçu pour gérer un tournoi d'échecs. Langage : python, mode terminal. Le programme suit le modèle de conception MVC : Models - View- Controller.

## Base de données

Les données sont stockées dans un fichier json générées à l'aide de TinyDB.
Le fichier nommé db.json se trouve dans data/tournaments/db.json

## Exigences

Les exigences pour lancer le programem se trouve dans le fichier requirements.txt. 

Voici les détails : 

flake8==7.0.0
flake8-html==0.4.3
Jinja2==3.1.3
markdown-it-py==3.0.0
MarkupSafe==2.1.5
mccabe==0.7.0
mdurl==0.1.2
pycodestyle==2.11.1
pyflakes==3.2.0
Pygments==2.17.2
python-dateutil==2.8.2
rich==13.7.0
six==1.16.0
tinydb==4.8.0

### Créez l'environement virtuel 

Pour cela exécuter la commande suivante : python -m venv venv

### Activez l'environement virtuel
#### Sous Windows.

\venv\Scripts\activate


### Installez les librairies requises
Ce script a été testé sur un **environnement Windows** à l'aide de PyCharm.  Les prérequis sont fournis dans le fichier Requirements.txt.  Pour obtenir exactement le même environnement de production, vous devez exécuter la commande suivante :

*pip install -r requirements.txt*

## Utilisation

Clonez le dépôt git :*git clone https://github.com/dogmatus07/ChessMasterTournament.git*

Accédez au répertoire du projet :*cd ChessMasterTournament*

Exécutez le script :*python main.py* pour lancer le programme.

## Fonctionnement

### 1. Création du tournoi

Commencez par créer le tournoi et à renseigner les informations le.concernant.
 
### 2. Création des joueurs
Créez ensuite les joueurs avec toutes les informations qui leur sont rattachées. 

### 3. Ajoutez les participants
Parmi les joueurs nouvellement créés, choisissez ceux qui vont participer au tournoi. 

Le programme est conçu pour gérer un tournoi à 4 rounds suivant le système suisse avec 8 joueurs. 

### 4. Démarrez le tournoi
Maintenant que vous avez un tournoi actif et des participants, vous pouvez démarrer le tournoi. 

Le programme va créer les rounds du tournoi, apparier les joueurs et créer les matches. 

### 5. Renseignez les résultats des matches
Le programme vous demandera de renseigner à chaque fois les résultats de chaque match et mettre à jour les scores des joueurs en conséquence. 

Les scores suivent la logique suivante : 
+ 1 point pour le gagnant
+ 0 point pour le perdant
+ 0.5 point en cas de match nul

### 6. Reprise d'un tournoi
A tout moment, l'utilisateur peut quitter le programme ou revenir au menu principal. Pour reprendre le tournoi, il suffit d'aller dans le menu gestion des rounds et choisir reprendre le tournoi. 

Le programme vous demandera quel tournoi et quel round et reprendra là où vous vous êtes arrêté. 

### Sauvegarde des données

Toutes les données sont sauvegardées au fur et à mesure que le programme s'exécute dans le fichier db.json

## Conformité PEP8 et rapport Flake8

Un rapport Flake8 a ete généré pour ce programme avec comme configuration une longueur de ligne à 119 maximum et une exclusion du dossier venv.
Cette configuration est définie dans le fichier .flake8

Le rapport au format html est présent dans le dossier flake8_report

Pour générer un nouveau rapport Flake8, effectuez la commande suivante dans le terminal : 

flake8 --format=html --htmldir=flake8_report .

## Clause de non-responsabilité
Ce programme sera utilisé à des fins éducatives uniquement.
