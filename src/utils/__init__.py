"""
Utility helpers for the Retail Analytics Platform.
Add reusable formatting, validation, or helper functions here.
"""

def format_currency(value: float, symbol: str = "R$") -> str:
    """Format a float as a currency string.

    Example:
        >>> format_currency(1234567.89)
        'R$ 1,234,567.89'
    """
    return f"{symbol} {value:,.2f}"


def format_millions(value: float, symbol: str = "R$") -> str:
    """Format a large float as a millions currency string.

    Example:
        >>> format_millions(16009240.95)
        'R$ 16.01 M'
    """
    return f"{symbol} {value / 1_000_000:.2f} M"
