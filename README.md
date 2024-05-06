# Recommandation_system_project_maching_learning

Ce projet est une implémentation d'un système de recommandation utilisant des techniques de machine learning. L'objectif principal est de recommander des articles ou des produits à des utilisateurs en se basant sur leurs historiques de notation ou de comportement.

# Fonctionnalités principales :

1. Implémentation de divers algorithmes de recommandation, tels que la factorisation matricielle, les modèles de filtrage collaboratif.

2. Utilisation de bibliothèques populaires telles que scikit-learn, Scipy et Surprise pour l'implémentation des modèles.

3. Prise en charge de différents types de données, y compris les données de notation utilisateur-article, les données de comportement utilisateur, et les métadonnées des articles.

4. Évaluation des performances des modèles à l'aide de mesures telles que RMSE, précision, rappel, et F-score.

5. Intégration d'une interface utilisateur pour permettre aux utilisateurs de découvrir et d'interagir avec les recommandations générées.

# Structure du projet :

### collaboratif_filttring_SVD.ipynb/
   un fichier pour l'algorithme de filtrage collaboratif utilisant la décomposition en valeurs singulières (SVD). 

### surprise_models.ipynb/ 
   un fichier contient le notebook Jupyter pour l'implémentation des modèles de la bibliothèque Surprise. 

### SGD_Model.ipynb/
   un fichier spécifique pour un notebook Jupyter contenant l'implémentation d'un modèle de descente de gradient stochastique (SGD) pour le système de recommandation.

### site_ecommerce_maching_learning/
    Le dossier contient une application web développée avec Django pour un système de recommandation sur un site e-commerce. L'application offre une interface utilisateur permettant aux utilisateurs de découvrir des produits recommandés en fonction de leurs préférences. Elle inclut des fonctionnalités telles que la page d'accueil, les recommandations personnalisées et les détails des produits.
### datasets/
   Le dossier `datasets/` contient trois ensembles de données distincts :
	- **Movies** : Un ensemble de données sur les films, comprenant des informations telles que les titres, les genres, les années de sortie et les évaluations.
	- **Electronics** : Un ensemble de données sur les produits électroniques, comprenant des informations telles que les noms des produits, les identifiants, les descriptions et les évaluations des utilisateurs.
	- **Software Electronics** : Un ensemble de données spécifique sur les logiciels électroniques, avec des informations similaires à l'ensemble de données sur l'électronique, mais se concentrant sur les produits logiciels.

# Comment exécuter le projet ?

Pour exécuter le projet, suivez ces étapes simples :

1. Assurez-vous d'avoir Python installé sur votre système Ubuntu. Vous pouvez installer Python en utilisant la commande suivante :
      ```bash
sudo apt update
sudo apt install python3
 ```
2. Clonez ce dépôt GitHub sur votre machine locale en utilisant la commande suivante dans votre terminal :
    ```bash             git clone <lien-du-dépôt>      
 ```
3. Naviguez vers le répertoire racine du projet :
    ```bash        cd <nom-du-dépôt>   
 ```
4. Installez les dépendances nécessaires en exécutant la commande suivante :
      ```bash      pip install <nom_biblio>
```
5. Exécutez l'application en utilisant la commande suivante :
       ```bash      python manage.py runserver
```
6. Accédez à l'URL fournie par Django dans votre navigateur pour accéder à l'application web.

C'est tout ! Vous devriez maintenant pouvoir utiliser et explorer l'application web sur votre machine locale.

# Exemple d'interface utilisateur:
Voici un exemple d'interface utilisateur de notre application web :
![Interface](https://www.cjoint.com/doc/24_05/NEgp4Sfcq7n_Capture-d%E2%80%99%C3%A9cran-2024-05-06-165515.png)



