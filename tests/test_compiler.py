import unittest
from compiler.transpiler import AlgoTranspiler
from compiler.errors import (
    CompileError,
    MissingEndError,
    MissingTypeError,
)

class TestAlgoTranspiler(unittest.TestCase):
    def setUp(self):
        self.transpiler = AlgoTranspiler()

    def test_simple_sum(self):
        algo = """
        ALGORITHME Somme
        DEBUT
          s <- 0
          Pour i de 1 à 10 Faire
            s <- s + i
          Fin Pour
          Ecrire_nl("Somme = ", s)
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        s, i   Entier
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_repeat_until(self):
        algo = """
        ALGORITHME TestRepeter
        DEBUT
          x <- 1
          Répéter
            x <- x * 2
          Jusqu'à x >= 16
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        x      Entier
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_selon_choices(self):
        algo = """
        ALGORITHME TestSelon
        DEBUT
          mois <- 2
          Selon mois
            1, 3, 5, 7, 8, 10, 12 : j <- 31
            4, 6, 9, 11 : j <- 30
            2 : j <- 28
            Sinon j <- 0
          Fin Selon
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        mois, j Entier
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_selon_multiline_and_nested_si(self):
        algo = """
        ALGORITHME Exercice
        DEBUT
          ecrire("Mois=")
          lire(m)
          Selon m
            1,3,5,7,8,10,12: j <- 31
            4,6,9,11: j <- 30
            2:
              ecrire("Année=")
              lire(a)
              Si (a MOD 4 == 0) Alors
                j <- 29
              Sinon
                j <- 28
              Finsi
            Sinon
              j <- -1
              ecrire("Mois Invalide : ", m)
          Fin Selon
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        m, j, a : Entier
        """
        py = self.transpiler.compile(algo)
        self.assertIn("case 2:", py)
        self.assertIn("if (a % 4 == 0):", py)
        self.assertIn("case _:", py)
        self.assertIn('print("Mois Invalide : ", m, end=\'\')', py)

        import builtins
        from unittest.mock import patch
        with patch.object(builtins, 'input', side_effect=['2', '2024']), patch('builtins.print'):
            ns = {'__name__': '__main__'}
            exec(py, ns)
        with patch.object(builtins, 'input', side_effect=['13']), patch('builtins.print') as mock_print:
            ns = {'__name__': '__main__'}
            exec(py, ns)
            mock_print.assert_any_call("Mois Invalide : ", 13, end='')

    def test_selon_nested_in_si_and_selon(self):
        algo = """
        ALGORITHME TestNestedSelon
        DEBUT
          x <- 1
          y <- 2
          Si x > 0 Alors
            Selon y
              1 : res <- 10
              2 :
                Selon x
                  1 : res <- 20
                  Sinon res <- 0
                Fin Selon
              Sinon
                res <- -1
            Fin Selon
          Sinon
            res <- -99
          Finsi
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        x, y, res : Entier
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_predefined_functions(self):
        algo = """
        ALGORITHME TestBuiltins
        DEBUT
          a <- Abs(-10)
          b <- RacineCarré(25)
          c <- Arrondi(4.6)
          ch <- "Informatique"
          l <- Long(ch)
          sub <- Sous_chaine(ch, 0, 4)
          maj <- Majus(sub)
          num <- Estnum("1234")
          val <- Valeur("42")
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        a, l, num, val : Entier
        b, c : Réel
        ch, sub, maj : Chaîne
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_array_operations(self):
        algo = """
        ALGORITHME TestTableau
        DEBUT
          T[0] <- 100
          T[1] <- 200
          T[2] <- T[0] + T[1]
        FIN
        Tableau de déclaration des objets
        Objet  Type / Nature
        T      Tableau de 10 Entier
        """
        py = self.transpiler.compile(algo)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_procedure_saisir_jusqua(self):
        algo = """
        Procedure saisir(@n:entier)
        Debut
          Repeter
          ecrire("N =")
          n <- 10
          jusqu'a(2 <= n <= 30)
        Fin
        Tableau de déclaration des objets locaux
        Objet  Type / Nature
        /      /

        ALGORITHME SommeDiviseurs
        DEBUT
          saisir(n)
          ecrire(n)
        FIN
        Tableau de déclaration des objets globaux
        Objet  Type / Nature
        saisir Procédure
        n      Entier
        """
        py = self.transpiler.compile(algo)
        self.assertIn("while True:", py)
        self.assertIn("if (2 <= n <= 30):", py)
        self.assertIn("break", py)
        self.assertIn("n = saisir(n)", py)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_players_ranking_compilation(self):
        with open("examples/players_ranking.algo", "r", encoding="utf-8") as f:
            algo = f.read()
        py = self.transpiler.compile(algo)
        self.assertIn("def _creer_Player", py)
        self.assertIn("def saisir(n):", py)
        self.assertIn("def registerPlayers(T, n):", py)
        self.assertIn("def playRounds(T, n, p):", py)
        self.assertIn("def determineRanking(T, n):", py)
        self.assertIn("T = array([_creer_Player() for _ in range(30)], dtype=object)", py)

    def test_string_array_preserves_full_strings(self):
        algo = """
        Procedure remplir(@T: Tableau de 5 Chaine)
        Debut
          T[0] <- "Hello World"
          T[1] <- "12345678"
        Fin
        Tableau de déclaration des objets locaux
        Objet  Type / Nature
        /      /

        ALGORITHME TestStringArray
        DEBUT
          remplir(T)
        FIN
        Tableau de déclaration des objets globaux
        Objet  Type / Nature
        remplir Procédure
        T      Tableau de 5 Chaine
        """
        py = self.transpiler.compile(algo)
        self.assertIn("T = array([''] * (5), dtype=object)", py)
        ns = {'__name__': '__main__'}
        exec(py, ns)

    def test_missing_end_blocks(self):
        # Missing Fin Pour
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nPour i de 1 à 10 Faire\nx <- i\nFIN\nTableau de déclaration des objets globaux\nx, i : Entier")
        self.assertIn("Fin Pour", str(cm.exception))

        # Missing Fin Tant que
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nTant que x < 10 Faire\nx <- x + 1\nFIN\nTableau de déclaration des objets globaux\nx : Entier")
        self.assertIn("Fin Tant que", str(cm.exception))

        # Missing Fin Si
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nSi x > 0 Alors\nx <- 0\nFIN\nTableau de déclaration des objets globaux\nx : Entier")
        self.assertIn("Fin Si", str(cm.exception))

        # Missing Jusqu'à
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nRépéter\nx <- x + 1\nFIN\nTableau de déclaration des objets globaux\nx : Entier")
        self.assertIn("Jusqu'à", str(cm.exception))

        # Missing Fin Selon
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nSelon x\n1 : x <- 2\nFIN\nTableau de déclaration des objets globaux\nx : Entier")
        self.assertIn("Fin Selon", str(cm.exception))

        # Missing FIN in subprogram
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("Procedure p()\nDEBUT\nx <- 1\nTableau de déclaration des objets locaux\n/\nALGORITHME T\nDEBUT\np()\nFIN\nTableau de déclaration des objets globaux\np: Procédure\nx : Entier")
        self.assertIn("FIN", str(cm.exception))

        # Missing FIN in ALGORITHME
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nx <- 1\nTableau de déclaration des objets globaux\nx : Entier")
        self.assertIn("FIN", str(cm.exception))

    def test_tantque_parenthesized_conditions(self):
        """Verifies tantque( and tantque ( with spaces in conditions compile and execute."""
        algo = """
        ALGORITHME TestTantQueParens
        DEBUT
          x <- 0
          tantque( x < 3 ) faire
            x <- x + 1
          Fin Tant que
          tantque ( x < 5 ) faire
            x <- x + 1
          Fin Tant que
          tantque(x < 6)faire
            x <- x + 1
          Fin Tant que
          Ecrire(x)
        FIN
        Tableau de déclaration des objets
        x : Entier
        """
        py = self.transpiler.compile(algo)
        self.assertIn("while ( x < 3 ):", py)
        self.assertIn("while ( x < 5 ):", py)
        self.assertIn("while (x < 6):", py)
        import io, contextlib
        buf = io.StringIO()
        ns = {'__name__': '__main__'}
        with contextlib.redirect_stdout(buf):
            exec(py, ns)
        self.assertEqual(buf.getvalue().strip(), "6")

        # Missing Fin Enregistrement
        with self.assertRaises(CompileError) as cm:
            self.transpiler.compile("ALGORITHME T\nDEBUT\nFIN\nTableau de déclaration des objets\n/\nDéclaration des types\nRec = Enregistrement\na: Entier")
        self.assertIn("Fin Enregistrement", str(cm.exception))

    def test_mandatory_end_enforcement(self):
        # Missing FIN without DEBUT
        with self.assertRaises(MissingEndError):
            self.transpiler.compile("ALGORITHME MonAlgo\nx <- 1\nTableau de déclaration des objets\nx : Entier")

        # Missing FIN with DEBUT
        with self.assertRaises(MissingEndError):
            self.transpiler.compile("ALGORITHME MonAlgo\nDEBUT\nx <- 1\nTableau de déclaration des objets\nx : Entier")

        # English END is accepted
        py = self.transpiler.compile("ALGORITHME MonAlgo\nDEBUT\nx <- 1\nEND\nTableau de déclaration des objets\nx : Entier")
        self.assertIn("x = 1", py)

    def test_mandatory_types_enforcement(self):
        # Undeclared variable in main
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile("ALGORITHME MonAlgo\nDEBUT\nx <- 1\nFIN\nTableau de déclaration des objets\n/")
        self.assertIn("non déclaré", str(cm.exception))

        # Missing TDO under main algorithm (no subprograms)
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile("ALGORITHME MonAlgo\nDEBUT\nx <- 1\nFIN")
        self.assertIn("TDO", str(cm.exception))

        # Missing TDOL after subprogram
        algo_no_tdol = """
        Procedure test(n: Entier)
        DEBUT
          ecrire(n)
        FIN
        ALGORITHME MonAlgo
        DEBUT
          test(5)
        FIN
        Tableau de déclaration des objets globaux
        test : Procédure
        """
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile(algo_no_tdol)
        self.assertIn("TDOL", str(cm.exception))

        # Undeclared variable in subprogram
        algo_sub = """
        Procedure test(n: Entier)
        DEBUT
          y <- n + 1
        FIN
        Tableau de déclaration des objets locaux
        /
        ALGORITHME MonAlgo
        DEBUT
          test(5)
        FIN
        Tableau de déclaration des objets globaux
        test : Procédure
        """
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile(algo_sub)
        self.assertIn("non déclaré", str(cm.exception))

        # Subprogram parameter missing type
        algo_param = """
        Procedure test(n)
        DEBUT
          ecrire(n)
        FIN
        Tableau de déclaration des objets locaux
        /
        ALGORITHME MonAlgo
        DEBUT
          test(5)
        FIN
        Tableau de déclaration des objets globaux
        test : Procédure
        """
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile(algo_param)
        self.assertIn("Type manquant pour le paramètre", str(cm.exception))

        # Function missing return type
        algo_fn = """
        Fonction carre(x: Entier)
        DEBUT
          retourner x * x
        FIN
        Tableau de déclaration des objets locaux
        /
        ALGORITHME MonAlgo
        DEBUT
          y <- carre(5)
        FIN
        Tableau de déclaration des objets globaux
        carre : Fonction
        y : Entier
        """
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile(algo_fn)
        self.assertIn("Type de retour obligatoire", str(cm.exception))

        # TDO item missing type
        algo_tdo = """
        ALGORITHME MonAlgo
        DEBUT
          x <- 1
        FIN
        Tableau de déclaration des objets
        Objet Type
        x
        """
        with self.assertRaises(MissingTypeError) as cm:
            self.transpiler.compile(algo_tdo)
        self.assertIn("Type manquant", str(cm.exception))

    def test_membership_interval_and_set_with_parens_and_logical_ops(self):
        """Verifies ∈ [a .. b] and ∈ {a, b} preserve outer parens and logical operators."""
        from compiler.expressions import ExpressionTranslator
        t = ExpressionTranslator()

        self.assertEqual(
            t.translate_expression('(Majus(ch[i]) ∈ ["A" .. "Z"] Ou ch[i] = " ")'),
            '(("A" <= Majus(ch[i]) <= "Z") or ch[i] == " ")',
        )
        self.assertEqual(
            t.translate_expression('ch[i] = " " Ou Majus(ch[i]) ∈ ["A" .. "Z"]'),
            'ch[i] == " " or ("A" <= Majus(ch[i]) <= "Z")',
        )
        self.assertEqual(
            t.translate_expression('a ∈ [1 .. 10] Et b ∈ [20 .. 30]'),
            '(1 <= a <= 10) and (20 <= b <= 30)',
        )
        self.assertEqual(
            t.translate_expression('Non x ∈ [1 .. 10]'),
            'not (1 <= x <= 10)',
        )
        self.assertEqual(
            t.translate_expression('(Majus(ch[i]) ∈ {"A", "E", "I"} Ou ch[i] = " ")'),
            '((Majus(ch[i]) in {"A", "E", "I"}) or ch[i] == " ")',
        )
        self.assertEqual(
            t.translate_expression('x ∈ [T[0] .. T[n - 1]]'),
            '(T[0] <= x <= T[n - 1])',
        )


if __name__ == '__main__':
    unittest.main()
