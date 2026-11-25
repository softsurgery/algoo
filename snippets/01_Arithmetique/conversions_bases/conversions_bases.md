# Conversions de Bases (Binaire, Octal, Hexadécimal ↔ Décimal)

## Description
Regroupe les fonctions dédiées à chaque base ainsi que les fonctions génériques pour toutes les bases (2 à 16) :
- **Binaire (base 2)** : `DecVersBinaire(n)` et `BinaireVersDec(ch)`
- **Octal (base 8)** : `DecVersOctal(n)` et `OctalVersDec(ch)`
- **Hexadécimal (base 16)** : `DecVersHexa(n)` et `HexaVersDec(ch)`
- **Générique (toutes bases)** : `DecVersBase(n, base)` et `BaseVersDec(ch, base)`

## Concepts Abordés
- Divisions successives (`Div`, `Mod`)
- Schéma de Horner (`res * base + v`)
- Manipulation de chaînes et caractères (`Long`, `Convch`, `Majus`, `Ord`)
- Structure à choix multiples `Selon` et intervalles (`∈`)
