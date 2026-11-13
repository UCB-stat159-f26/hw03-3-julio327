"""Plot career match age differences."""


def plot_career(data):
    """Plot player age against the age difference for each match."""
    import matplotlib.pyplot as plt

    required = {"player_age", "age_difference", "result"}
    if not required.issubset(data.columns):
        raise ValueError(
            "Data must include player_age, age_difference, and result."
        )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for result, color, label in [
        ("W", "#2b8cbe", "Win"),
        ("L", "#e34a33", "Loss"),
    ]:
        matches = data[data["result"] == result]
        ax.scatter(
            matches["player_age"],
            matches["age_difference"],
            color=color,
            label=label,
            alpha=0.65,
            s=24,
        )

    ax.axhline(0, color="#666666", linewidth=0.8)
    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Player age − opponent age (years)")
    ax.legend(frameon=False, title="Match result")
    fig.tight_layout()
    return ax
