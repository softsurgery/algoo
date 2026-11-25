# Codes ASCII avec `Ord` et `Chr`

## Description
Illustre l'utilisation des fonctions prédéfinies `Ord(c)` (caractère → code ASCII) et `Chr(code)` (code ASCII → caractère) :
- Affichage du code ASCII de chaque caractère d'une chaîne avec `Ord`.
- Génération de l'alphabet majuscule (`65` à `90`) avec `Chr`.
- Conversion manuelle des lettres minuscules (`'a'..'z'`) en majuscules (`'A'..'Z'`) par décalage ASCII (`Ord(c) - 32`).

## Concepts Abordés
- Fonctions `Ord` et `Chr`
- Appartenance à un intervalle de caractères (`c ∈ ["a" .. "z"]`)
- Parcours d'une chaîne de `0` à `Long(ch) - 1`
