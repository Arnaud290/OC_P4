++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# PROJET 4 : Développez un programme logiciel en Python

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Contexte

Création d'un logiciel en langage Python permettant d'effectuer la gestion de tournois d'échecs au format suisse.
Ce logiciel s'exécute depuis une console sur Windows, Linux ou MacOs, il est conçu selon le modèle MVC.


## Installation


### 1 - Installation de Python3, l'outil d'environnement virtuel et le gestionnaire de paquets (sur Linux UBUNTU)
    

    $ sudo apt-get install python3 python3-venv python3-pip


### 2 - Mise en place de l'environnement virtuel "env"


    1 - Accès au répertoire du projet :
            
            exemple cd /chess

    2 - Création de l'environnement virtuel :
            
            $ python3 -m venv env


### 3 - Ouverture de l'environnement virtuel et ajout des modules


            $ source env/bin/activate
            
            (env) $ pip install -r requirements.txt
            

## Utilisation du programme


### 1 - Lancement


            $ python3 main.py


### 2 - Utilisation


    1 - CHESS MAIN MENU

            1 - création d'un nouveau tournoi ou reprise d'un tournoi en cours
            2 - Création et gestion des joueurs
            3 - Visualisation des rapports des tournois

    2 - NEW TOURNAMENT

            Créer un tournoi en répondant aux questions (nom du tournoi, lieu, ...).
            Le nombre de joueurs est de 8 par défaut mais peut être modifié avec un autre nombre pair.
            Le nombre de rounds est de 4 par défaut mais peut être augmenté à (nombre de joueurs - 1)

    3 - TOURNAMENT PLAYERS

            Possibilité d'ajouter, d'enlever ou de modifier les caractéristiques des joueurs avant le début du tournoi.
            Lancement du tournoi.

    4 - TOURNAMENT

            Visuel des tours et gestion des matchs en indiquant les résultats des joueurs.
            Possibilité de supprimer le tournoi en cours.

    5 - MANAGE PLAYERS

            Visuel des joueurs selon l'ordre alphabetique, l'id ou le rang.
            Possibilité de créer des joueurs et de modifier les caractéristiques

    5 - RAPPORTS

            Visuel de tous les tournois. 
            Visuel des joueurs d'un tournoi selon l'ordre alphabétique, les points de matchs ou le rang.
            Visuel des tours et des matchs.


### 3 - Génération d'un rapport FLAKE8


            1 - $ source env/bin/activate
            2 - (env) $ flake8
                
            Le fichier .flake8 présent dans le repertoire contient la configuration de flake8