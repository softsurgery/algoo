# Affichage Récursif d'un Tableau (2 Méthodes)

## Description
Affiche les `n` éléments d'un tableau `T` par récursivité selon deux approches :
1. **Avec compteur `i`** (`AfficherRecCompteur(T, n, i)`) : affiche `T[i]` puis avance avec `i + 1` jusqu'à `i = n`.
2. **En tronquant la taille `n`** (`AfficherRecTronquer(T, n)`) : descend récursivement sur `n - 1` puis affiche `T[n - 1]` au retour pour conserver l'ordre `0 .. n - 1`.

## Concepts Abordés
- Procédures récursives sur tableaux
- Récursivité terminale vs récursivité avec traitement au retour
- Déclaration de type tableau (`Tab`) dans le TDNT
