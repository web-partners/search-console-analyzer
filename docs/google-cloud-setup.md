# Configuration des identifiants Google Cloud

Ce guide détaille la procédure pour obtenir les identifiants nécessaires à l'utilisation de l'API Google Search Console.

## 1. Accéder à la Google Cloud Console

1. Ouvrez votre navigateur et rendez-vous sur [Google Cloud Console](https://console.cloud.google.com/)
2. Connectez-vous avec votre compte Google qui gère la Search Console

## 2. Créer ou sélectionner un projet

1. Cliquez sur le sélecteur de projet en haut de la page
2. Pour créer un nouveau projet :
   - Cliquez sur "Nouveau projet"
   - Donnez un nom explicite à votre projet
   - Cliquez sur "Créer"
3. Pour utiliser un projet existant :
   - Sélectionnez-le dans la liste

## 3. Activer l'API Search Console

1. Dans le menu latéral, naviguez vers "APIs & Services" > "Bibliothèque"
2. Recherchez "Google Search Console API"
3. Cliquez sur l'API dans les résultats
4. Cliquez sur "Activer"

## 4. Créer un compte de service

1. Dans le menu latéral, allez dans "APIs & Services" > "Identifiants"
2. Cliquez sur "Créer des identifiants" > "Compte de service"
3. Remplissez les informations :
   - Nom du compte de service (ex: "search-console-analyzer")
   - Description (optionnelle)
   - Cliquez sur "Créer"
4. Vous pouvez ignorer l'attribution de rôles (cliquez "Continuer")
5. Cliquez sur "Terminé"

## 5. Générer la clé JSON

1. Dans la liste des comptes de service, trouvez celui que vous venez de créer
2. Cliquez sur les trois points verticaux (⋮) > "Gérer les clés"
3. Cliquez sur "Ajouter une clé" > "Créer une clé"
4. Sélectionnez le format "JSON"
5. Cliquez sur "Créer"
   - Le fichier JSON sera automatiquement téléchargé

## 6. Configurer l'accès Search Console

1. Copiez l'adresse email du compte de service depuis le fichier JSON (`client_email`)
2. Ouvrez [Google Search Console](https://search.google.com/search-console)
3. Sélectionnez votre propriété
4. Cliquez sur "Paramètres" (⚙️) > "Utilisateurs et autorisations"
5. Cliquez sur "Ajouter un utilisateur"
6. Collez l'adresse email du compte de service
7. Sélectionnez le niveau d'accès "Propriétaire"
8. Validez

## 7. Sécuriser vos identifiants

1. Renommez le fichier JSON téléchargé en `credentials.json`
2. Placez-le dans le dossier `config/` de votre projet
3. **IMPORTANT** : 
   - N'incluez JAMAIS ce fichier dans un dépôt Git
   - Ajoutez `config/credentials.json` à votre `.gitignore`
   - Conservez une copie sécurisée du fichier

## Vérification

Pour vérifier que tout fonctionne :

1. Assurez-vous que le fichier `credentials.json` est dans le bon dossier
2. Exécutez le script avec les paramètres de base
3. Si vous obtenez des erreurs d'authentification :
   - Vérifiez que l'API est bien activée
   - Confirmez que le compte de service a accès à la Search Console
   - Validez le format de l'URL de votre site