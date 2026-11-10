"""Generate shareable archive charts from the public price dataset."""

import json
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

DOCS = Path(__file__).resolve().parents[1] / "docs"
LONDON = ZoneInfo("Europe/London")
DIRECTIONS = ("import", "export")
TEAL, ORANGE = "#097B72", "#AC5315"
INK, MUTED = "#182C34", "#4F636D"


def midnight(day):
    return int(datetime.combine(day, time.min, LONDON).timestamp())


def complete_days(data):
    grouped = {channel: defaultdict(list) for channel in DIRECTIONS}
    for channel, days in grouped.items():
        for row in data["channels"][channel]:
            if row["quality"] == "history":
                days[date.fromisoformat(row["day"])].append(row)
    complete = {}
    for day in sorted(set(grouped["import"]) & set(grouped["export"])):
        starts = list(range(midnight(day), midnight(day + timedelta(days=1)), 1800))
        rows = {channel: sorted(grouped[channel][day], key=lambda row: row["start"])
                for channel in DIRECTIONS}
        if all([row["start"] for row in channel] == starts and
               all(row["end"] == row["start"] + 1800 for row in channel)
               for channel in rows.values()):
            complete[day] = rows
    return complete


def profile(days, channel):
    by_slot = [[] for _ in range(48)]
    for channels in days:
        local_slots = defaultdict(list)
        for row in channels[channel]:
            local = datetime.fromtimestamp(row["start"], LONDON)
            local_slots[local.hour * 2 + local.minute // 30].append(row["latest"])
        for slot, values in local_slots.items():
            by_slot[slot].append(mean(values))
    return [mean(values) for values in by_slot]


def figure(title, subtitle, note):
    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7.5), dpi=160)
    fig.subplots_adjust(left=.105, right=.95, top=.78, bottom=.15, hspace=.46)
    fig.text(.085, .943, title, fontsize=25, weight="bold", color=INK)
    fig.text(.085, .897, subtitle, fontsize=12.5, color=MUTED)
    fig.text(.085, .077, note, fontsize=10.5, color=MUTED)
    fig.text(.085, .044, "North West England · Early Bird Booster included · Optimise Price Watch",
             fontsize=10, color=MUTED)
    for channel, ax in zip(DIRECTIONS, axes):
        ax.set_title(f"{channel.title()} prices", loc="left", weight="bold", color=INK, pad=9)
        ax.set_ylabel("p/kWh", color=MUTED)
        ax.tick_params(length=0, pad=7, labelcolor=MUTED)
        ax.spines[:].set_visible(False)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color="#e0e8e7")
        ax.axhline(0, color="#91a4aa", lw=.75)
    return fig, axes


def main():
    data = json.loads((DOCS / "data" / "north-west.json").read_text(encoding="utf-8"))
    complete = complete_days(data)
    dates = list(complete)
    period = f"{dates[0]:%d %b}–{dates[-1]:%d %b %Y} · {len(dates)} complete days"
    path = DOCS / "charts"
    path.mkdir(exist_ok=True)

    fig, axes = figure("How far did prices move each day?",
                       f"E.ON Next Optimise · {period}",
                       "Each bar spans the lowest and highest observed half-hour. Shading marks weekends.")
    for channel, ax, color in zip(DIRECTIONS, axes, (TEAL, ORANGE)):
        prices = [[row["latest"] for row in complete[day][channel]] for day in dates]
        for day in dates:
            if day.weekday() == 5:
                ax.axvspan(mdates.date2num(day) - .5, mdates.date2num(day) + 1.5,
                           color="#edf3f3", zorder=0)
        lows, highs = list(map(min, prices)), list(map(max, prices))
        ax.vlines(dates, lows, highs, color=color, lw=2.5, alpha=.8)
        ax.scatter(dates, lows, s=12, color=color)
        ax.scatter(dates, highs, s=12, color=color)
        ax.set_xlim(mdates.date2num(dates[0]) - 1, mdates.date2num(dates[-1]) + 1)
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        print(channel, "historical min/max:", min(lows), max(highs),
              "days with a negative slot:", sum(value < 0 for value in lows))
    fig.savefig(path / "optimise-daily-price-range.png")
    plt.close(fig)

    fig, axes = figure("When were prices usually lowest?",
                       f"E.ON Next Optimise · {period} · UK local time",
                       "Each day counts once. The repeated autumn clock-change slots are averaged within that day.")
    handles = []
    for weekend, color in ((False, TEAL), (True, ORANGE)):
        group = [rows for day, rows in complete.items() if (day.weekday() >= 5) == weekend]
        label = "Weekends" if weekend else "Weekdays"
        handles.append(Line2D([0], [0], color=color, lw=2.5, label=f"{label} · {len(group)} days"))
        for channel, ax in zip(DIRECTIONS, axes):
            values = profile(group, channel)
            ax.stairs(values, [i / 2 for i in range(49)], baseline=None, color=color, lw=2.2)
            low = min(range(48), key=values.__getitem__)
            high = max(range(48), key=values.__getitem__)
            print(label, channel, "low / high:", [(f"{i // 2:02d}:{i % 2 * 30:02d}",
                  round(values[i], 2)) for i in (low, high)])
            ax.set_xlim(0, 24)
            ax.set_xticks(range(0, 25, 3), [f"{h:02d}:00" for h in range(0, 25, 3)])
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(.079, .872),
               ncol=2, frameon=False, fontsize=11)
    fig.savefig(path / "optimise-weekday-weekend-profile.png")
    plt.close(fig)
    print(period)


if __name__ == "__main__":
    main()
