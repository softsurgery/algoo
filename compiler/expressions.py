"""
Algorithmic Expression and Target Translator.
"""

import re

class ExpressionTranslator:
    """Translates algorithmic expressions and assignment targets to valid Python 3 expressions."""

    def __init__(self):
        self.fn_map = {
            'arrondi': 'Arrondi',
            'racinecarré': 'RacineCarré',
            'racinecarre': 'RacineCarré',
            'aléa': 'Aléa',
            'alea': 'Aléa',
            'ent': 'Ent',
            'abs': 'Abs',
            'ord': 'Ord',
            'chr': 'Chr',
            'long': 'Long',
            'pos': 'Pos',
            'convch': 'Convch',
            'estnum': 'Estnum',
            'valeur': 'Valeur',
            'sous_chaine': 'Sous_chaine',
            'effacer': 'Effacer',
            'majus': 'Majus',
            'fin_fichier': '_fin_fichier',
            'finfichier': '_fin_fichier',
            'ouvrir': 'Ouvrir',
            'lire_ligne': 'Lire_ligne',
            'lireligne': 'Lire_ligne',
        }

    def translate_target(self, target_str: str) -> str:
        """Translates target expression for assignment LHS (e.g. M[i, j], E.champ, T[i].champ)."""
        target = target_str.strip()

        # Handle indexed record field: T[i].field -> T[i]['field']
        m_idx_dot = re.match(r'^([a-zA-Z0-9_]+\[.+?\])\.([a-zA-Z0-9_]+)$', target)
        if m_idx_dot:
            base = self.translate_target(m_idx_dot.group(1))
            return f"{base}['{m_idx_dot.group(2)}']"

        # Handle 2D index: M[i, j] -> M[i, j] (numpy array)
        m_2d = re.match(r'^([a-zA-Z0-9_]+)\s*\[\s*(.+?)\s*,\s*(.+?)\s*\]$', target)
        if m_2d:
            arr = m_2d.group(1)
            i_idx = self.translate_expression(m_2d.group(2))
            j_idx = self.translate_expression(m_2d.group(3))
            return f"{arr}[{i_idx}, {j_idx}]"

        # Handle 1D index: T[i]
        m_1d = re.match(r'^([a-zA-Z0-9_]+)\s*\[\s*(.+?)\s*\]$', target)
        if m_1d:
            arr = m_1d.group(1)
            i_idx = self.translate_expression(m_1d.group(2))
            return f"{arr}[{i_idx}]"

        # Handle record field: E.champ -> E['champ']
        if '.' in target:
            parts = target.split('.', 1)
            return f"{parts[0]}['{parts[1]}']"

        return target

    def translate_expression(self, expr_str: str) -> str:
        """
        Translates algorithmic expressions to Python expressions:
        - Operators: Div -> //, Mod -> %, Et -> and, Ou -> or, Non -> not
        - Equality: = -> ==, ≠ / <> -> !=, ≤ -> <=, ≥ -> >=
        - Sets & Intervals: x  [a .. b] -> (a <= x <= b), x  {a, b} -> (x in {a, b})
        - Built-in functions mapping
        - Record dot access: E.champ -> E['champ']
        """
        if not expr_str:
            return ""

        # Protect string literals from token replacement
        str_map = {}
        str_idx = 0

        def save_str(m):
            nonlocal str_idx
            placeholder = f"__STR_{str_idx}__"
            str_map[placeholder] = m.group(0)
            str_idx += 1
            return placeholder

        # Match single or double quoted strings
        s = re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', save_str, expr_str)

        # Handle membership in intervals (expr ∈ [a .. b]) and sets (expr ∈ {a, b, c})
        s = self._translate_membership(s)

        # Handle 2D index in expressions: M[i, j]
        s = re.sub(r'([a-zA-Z0-9_]+)\s*\[\s*(.+?)\s*,\s*(.+?)\s*\]', r'\1[\2, \3]', s)

        # Handle predefined function names (case-insensitive)
        for fn_name, py_fn in self.fn_map.items():
            s = re.sub(rf'\b{fn_name}\s*\(', f'{py_fn}(', s, flags=re.IGNORECASE)

        # Handle Boolean literals
        s = re.sub(r'\bvrai\b', 'True', s, flags=re.IGNORECASE)
        s = re.sub(r'\bfaux\b', 'False', s, flags=re.IGNORECASE)

        # Handle arithmetic and logical operators
        s = re.sub(r'\bdiv\b', '//', s, flags=re.IGNORECASE)
        s = re.sub(r'\bmod\b', '%', s, flags=re.IGNORECASE)
        s = re.sub(r'\bet\b', 'and', s, flags=re.IGNORECASE)
        s = re.sub(r'\bou\b', 'or', s, flags=re.IGNORECASE)
        s = re.sub(r'\bnon\b', 'not', s, flags=re.IGNORECASE)
        s = re.sub(r'\bdans\b', 'in', s, flags=re.IGNORECASE)

        # Comparison operators
        s = s.replace('≠', '!=').replace('<>', '!=')
        s = s.replace('≤', '<=')
        s = s.replace('≥', '>=')
        s = s.replace('', ' in ').replace('∈', ' in ')

        # Handle equality '=' -> '==' (when not part of <=, >=, !=, ==)
        s = re.sub(r'(?<![<>!=])=(?![=])', '==', s)

        # Handle record dot access: E.champ -> E['champ']
        def replace_dot(m):
            obj = m.group(1)
            field = m.group(2)
            return f"{obj}['{field}']"

        s = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\b', replace_dot, s)

        # Restore strings
        for placeholder, original in str_map.items():
            s = s.replace(placeholder, original)

        return s

    @staticmethod
    def _find_matching_closer(s: str, open_idx: int, close_ch: str) -> int:
        """Find the index of the matching closer for s[open_idx], or -1 if unmatched."""
        depth = 0
        for i in range(open_idx, len(s)):
            ch = s[i]
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
                if depth == 0:
                    return i if ch == close_ch else -1
                if depth < 0:
                    return -1
        return -1

    @staticmethod
    def _find_lhs_start(s: str, end_idx: int) -> int:
        """Scan backwards from end_idx to find the start of the LHS operand of ∈/dans/in."""
        depth = 0
        i = end_idx - 1
        while i >= 0:
            ch = s[i]
            if ch in ')]}':
                depth += 1
                i -= 1
                continue
            if ch in '([{':
                if depth > 0:
                    depth -= 1
                    i -= 1
                    continue
                return i + 1
            if depth == 0:
                if ch in (',', '=', '<', '>', '≤', '≥', '≠', ':'):
                    return i + 1
                if ch.isalnum() or ch == '_':
                    j = i
                    while j > 0 and (s[j - 1].isalnum() or s[j - 1] == '_'):
                        j -= 1
                    if s[j:i + 1].lower() in ('et', 'ou', 'non', 'and', 'or', 'not'):
                        return i + 1
                    i = j - 1
                    continue
            i -= 1
        return 0

    @staticmethod
    def _find_top_level_dotdot(s: str) -> int:
        """Find the index of '..' at bracket/paren depth 0, or -1 if not found."""
        depth = 0
        i = 0
        while i < len(s) - 1:
            ch = s[i]
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth = max(0, depth - 1)
            elif depth == 0 and s[i:i + 2] == '..':
                return i
            i += 1
        return -1

    @staticmethod
    def _split_top_level_commas(s: str) -> list:
        """Split s on commas at bracket/paren depth 0."""
        parts = []
        depth = 0
        start = 0
        for i, ch in enumerate(s):
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth = max(0, depth - 1)
            elif ch == ',' and depth == 0:
                parts.append(s[start:i])
                start = i + 1
        parts.append(s[start:])
        return parts

    def _translate_membership(self, s: str) -> str:
        """Translate all interval (∈ [a .. b]) and set (∈ {a, b}) membership expressions."""
        pattern = re.compile(r'\s+(?:|∈|dans|in)\s+([\[{])', re.IGNORECASE)
        search_pos = 0
        while True:
            m = pattern.search(s, search_pos)
            if not m:
                break
            opener = m.group(1)
            closer = ']' if opener == '[' else '}'
            opener_idx = m.end() - 1
            closer_idx = self._find_matching_closer(s, opener_idx, closer)
            if closer_idx == -1:
                search_pos = m.end()
                continue

            val_start = self._find_lhs_start(s, m.start())
            while val_start < m.start() and s[val_start].isspace():
                val_start += 1
            val_str = s[val_start:m.start()].strip()
            if not val_str:
                search_pos = m.end()
                continue

            rhs_inner = s[opener_idx + 1:closer_idx]
            if opener == '[':
                dotdot_idx = self._find_top_level_dotdot(rhs_inner)
                if dotdot_idx == -1:
                    search_pos = m.end()
                    continue
                val = self.translate_expression(val_str)
                low = self.translate_expression(rhs_inner[:dotdot_idx].strip())
                high = self.translate_expression(rhs_inner[dotdot_idx + 2:].strip())
                replacement = f"({low} <= {val} <= {high})"
            else:
                val = self.translate_expression(val_str)
                items = [
                    self.translate_expression(it.strip())
                    for it in self._split_top_level_commas(rhs_inner)
                    if it.strip()
                ]
                replacement = f"({val} in {{{', '.join(items)}}})"

            s = s[:val_start] + replacement + s[closer_idx + 1:]
            search_pos = val_start + len(replacement)
        return s
