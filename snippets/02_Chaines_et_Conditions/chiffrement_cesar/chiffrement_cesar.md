# Chiffrement de César

## Description
Implémente le chiffrement et le déchiffrement de César avec un décalage `k` :
- `ChiffrerCesar(ch, k)` : décale chaque lettre majuscule (`"A".."Z"`) ou minuscule (`"a".."z"`) de `k` positions modulo 26 à l'aide de `Ord` et `Chr`, tout en conservant les autres caractères (espaces, ponctuation).
- `DechiffrerCesar(ch, k)` : applique le décalage inverse `26 - (k Mod 26)` pour retrouver le message original.

## Concepts Abordés
- Arithmétique modulaire (`Mod 26`)
- Manipulation ASCII (`Ord` et `Chr`)
- Conditions imbriquées (`Si ... Sinon Si ... Sinon`) et intervalles (`∈`)
