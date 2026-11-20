"""Trip and budget optimization algorithm."""


def parse_options(raw_options: list[dict]) -> list[dict]:
    """Validate and normalize raw trip options.

    Args:
        raw_options: List of dictionaries containing origin, destination,
            base_price, and baggage_fee.

    Returns:
        List of cleaned option dictionaries with float prices.
    """
    cleaned: list[dict] = []
    for item in raw_options:
        # Ensure numeric fields are non-negative floats
        base_price = float(item["base_price"])
        baggage_fee = float(item["baggage_fee"])
        if base_price < 0 or baggage_fee < 0:
            raise ValueError("Prices and fees must be non-negative.")

        cleaned.append(
            {
                "origin": str(item["origin"]).strip(),
                "destination": str(item["destination"]).strip(),
                "base_price": base_price,
                "baggage_fee": baggage_fee,
            }
        )
    return cleaned


def apply_discount(options: list[dict], discount_rate: float) -> list[dict]:
    """Apply a proportional discount rate (0.0 to 1.0) to total option cost.

    Args:
        options: List of validated option dictionaries.
        discount_rate: Discount ratio between 0.0 and 1.0 (e.g., 0.10 for 10%).

    Returns:
        List of options including a rounded 'final_price' field.
    """
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("discount_rate must be between 0.0 and 1.0.")

    discounted: list[dict] = []
    for item in options:
        # Combine base price and baggage fee before applying discount
        gross_cost = item["base_price"] + item["baggage_fee"]
        final_price = round(gross_cost * (1.0 - discount_rate), 2)
        discounted.append({**item, "final_price": final_price})
    return discounted


def filter_and_sort(options: list[dict], max_budget: float) -> list[dict]:
    """Filter options within budget and sort ascending by final price.

    Args:
        options: List of option dictionaries with 'final_price'.
        max_budget: Maximum allowed final price.

    Returns:
        Filtered and sorted list of options within budget.
    """
    if max_budget < 0:
        raise ValueError("max_budget must be non-negative.")

    within_budget = [
        item for item in options if item["final_price"] <= max_budget
    ]
    # Sort from lowest to highest final price
    return sorted(within_budget, key=lambda x: x["final_price"])


def format_report(options: list[dict]) -> str:
    """Format ranked options into a readable summary string.

    Args:
        options: Sorted list of valid options with 'final_price'.

    Returns:
        Human-readable summary of valid options.
    """
    if not options:
        return "No options match the given budget."

    lines = ["Ranked options within budget:"]
    for idx, item in enumerate(options, start=1):
        lines.append(
            f"{idx}. {item['origin']} -> {item['destination']}: "
            f"{item['final_price']:.2f}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    sample_options = [
        {"origin": "LPA", "destination": "MAD", "base_price": 100.0, "baggage_fee": 25.0},
        {"origin": "LPA", "destination": "BCN", "base_price": 130.0, "baggage_fee": 20.0},
        {"origin": "LPA", "destination": "TFN", "base_price": 50.0, "baggage_fee": 10.0},
    ]
    parsed = parse_options(sample_options)
    discounted = apply_discount(parsed, discount_rate=0.10)
    ranked = filter_and_sort(discounted, max_budget=120.0)
    print(format_report(ranked))
