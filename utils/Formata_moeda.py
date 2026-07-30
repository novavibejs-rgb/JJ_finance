def moeda(valor):
        """Formata moeda brasileira."""

        try:
            valor = float(valor)
            return (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        except (ValueError, TypeError):
            return "R$ 0,00"
