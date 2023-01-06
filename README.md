# LITReview

Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

→ Développement d'une application Web avec **Django**

## Présentation de l'application

*LITReview* est une application permettant de mettre en relation des lecteurs souhaitant échanger leurs avis au sujet de livres.

Les utilisateurs ont la possibilité de :
- créer une critique au sujet d'un livre en particulier ;
- solliciter une critique pour un livre donné ;
- s'abonner ou se désabonner à d'autres utilisateurs afin de se tenir au courant des sollicitations et critiques publiées par ces derniers.

## Lancement de l'application
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- lancer le serveur de développement : python manage.py runserver
- se rendre à l'adresse : http://127.0.0.1:8000/

<ins>Note :</ins>  
Pour faciliter la découverte de l'application, la base de données db.slite3 est incluse dans le dépôt. Plusieurs comptes ont déjà été créés avec toujours le même mot de passe : **mdptest123**. L'utilisateur admin est **Roman**.