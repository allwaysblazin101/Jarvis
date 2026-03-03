
import sympy as sp


def solve_math_expression(text: str):

    try:
        # Extract math expression
        expression = ''.join(
            c for c in text if c.isdigit() or c in "+-*/(). "
        )

        if not expression:
            return None

        result = sp.sympify(expression).evalf()

        return float(result)

    except:
        return None

