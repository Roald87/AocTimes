import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Source https://github.com/mevdschee/aoc-stats
scores = pd.read_csv("scores.csv")

days = scores["day"].max()
cubehelix_kwargs = dict(n_colors=days, rot=-.25, light=.7, dark=.2)
color_star1 = sns.cubehelix_palette(start=1, **cubehelix_kwargs)
color_star2 = sns.cubehelix_palette(**cubehelix_kwargs)

for year in scores["year"].unique():
    f, axs = plt.subplots(days, 1, figsize=(10, 10), sharex=True, sharey=True)
    for (stars, day), times in scores.query(f'year == {year}').groupby("stars day".split()):
        ax = axs[day - 1]

        # plot kernel density estimate (kde)
        color = color_star1[day - 1] if stars == 1 else color_star2[day - 1]
        kdeplot_kwargs = dict(x=times["seconds"], ax=ax, clip_on=False, alpha=0.8, clip=(0, 5000))
        sns.kdeplot(**kdeplot_kwargs, fill=True, color=color)
        # kde outline
        sns.kdeplot(**kdeplot_kwargs, color="w", linewidth=1)

        # hide all ticks except for the last graphs x-axis
        ax.get_yaxis().set_visible(False)
        if day < 25:
            ax.get_xaxis().set_visible(False)

        # hide all spines
        for side in "top bottom left right".split():
            ax.spines[side].set_visible(False)

        ax.patch.set_alpha(0)

        # day labels
        if stars == 1:
            d = day if day > 1 else "day 1"
            ax.text(-20, 0, d, ha='right', color=color, fontdict=dict(weight='bold'))

    f.tight_layout()
    f.subplots_adjust(hspace=-0.9, left=0.05)
    plt.suptitle("Top 100 times of part 1 and 2 of Advent of Code", y=0.75)
    axs[0].text(5000*0.95, 0, year, fontdict=dict(fontsize=30, fontweight='bold'), ha='right')
    plt.xlim(0, 5000)
    plt.savefig(f"{year}.png")
    plt.show()
