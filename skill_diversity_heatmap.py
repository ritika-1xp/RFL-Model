from __future__ import annotations

import os
from typing import Dict, List, Tuple

import plotly.graph_objects as go


class SkillEntry:
    def __init__(self, skill: str, current_pct: float, target_pct: float):
        self.skill = skill
        self.current_pct = current_pct
        self.target_pct = target_pct

    @property
    def gap_pct(self) -> float:
        return self.current_pct - self.target_pct

    @property
    def gap_hours_1000h(self) -> float:
        return self.gap_pct * 10.0

    @property
    def heatmap_status(self) -> Tuple[str, str]:
        if abs(self.gap_pct) <= 0.75:
            return "green", "on target"
        if self.gap_pct > 0:
            return "blue", "reduce"
        return "red", "collect more"

    def summary(self) -> Dict[str, object]:
        color, action = self.heatmap_status
        return {
            "skill": self.skill,
            "current_pct": self.current_pct,
            "target_pct": self.target_pct,
            "gap_pct": self.gap_pct,
            "gap_hours_1000h": self.gap_hours_1000h,
            "heatmap_color": color,
            "action": action,
        }


SKILLS: List[SkillEntry] = [
    SkillEntry("Assembly & Installation", 20.7, 5.6),
    SkillEntry("Tool Use & Technical Manipulation", 12.3, 6.6),
    SkillEntry("Electronics & Diagnostics", 2.1, 7.0),
    SkillEntry("Healthcare & Caregiving", 0.0, 4.9),
    SkillEntry("Repair & Maintenance", 1.5, 6.3),
    SkillEntry("Agriculture & Farm Work", 4.3, 0.0),
    SkillEntry("Dish Handling", 0.6, 4.7),
    SkillEntry("Retail & Service Operations", 2.5, 6.2),
    SkillEntry("Human Interaction & Handoffs", 0.0, 3.5),
    SkillEntry("Home Appliance Interaction", 0.2, 3.7),
    SkillEntry("Food Preparation & Cooking", 10.3, 7.9),
    SkillEntry("Pick and Place / Object Handling", 2.1, 4.0),
    SkillEntry("Inventory & Stock Management", 7.0, 5.3),
    SkillEntry("Mechanical / Automotive Work", 5.8, 7.4),
    SkillEntry("Packing & Bagging", 6.1, 5.2),
    SkillEntry("Clothing & Laundry", 6.1, 5.2),
    SkillEntry("Organization & Tidying", 5.5, 4.7),
    SkillEntry("Construction & Building", 7.7, 7.0),
    SkillEntry("Cleaning & Sanitation", 5.1, 5.1),
]


def build_gap_matrix(entries: List[SkillEntry]) -> Tuple[List[str], List[float], List[str]]:
    labels = [e.skill for e in entries]
    values = [e.gap_pct for e in entries]
    annotations = [
        f"{e.skill}<br>Current: {e.current_pct:.1f}%<br>Target: {e.target_pct:.1f}%<br>Gap: {e.gap_pct:+.1f}%"
        for e in entries
    ]
    return labels, values, annotations


def build_figure(entries: List[SkillEntry]):
    labels, values, annotations = build_gap_matrix(entries)

    fig = go.Figure(
        data=go.Heatmap(
            z=[values],
            x=labels,
            y=["Gap from target (%)"],
            text=[annotations],
            texttemplate="%{text}",
            hovertemplate="<b>%{x}</b><br>Gap: %{z:+.1f}%<extra></extra>",
            colorscale=[
                [0.0, "#d9534f"],  # red (under target)
                [0.48, "#d9e7c9"],
                [0.5, "#a7d89d"],  # green (on target)
                [0.52, "#d9edf7"],
                [1.0, "#5b8bd4"],  # blue (over target)
            ],
            zmin=-15,
            zmax=15,
            zmid=0,
            showscale=True,
            colorbar=dict(
                title="Gap %",
                tickmode="array",
                tickvals=[-15, -10, -5, 0, 5, 10, 15],
                ticktext=["-15", "-10", "-5", "0", "+5", "+10", "+15"],
            ),
        )
    )

    fig.update_layout(
        title="Skill Group Target Heatmap (1000-hour dataset)",
        xaxis=dict(
            tickangle=0,
            showticklabels=True,
            tickfont=dict(size=11),
            side="top",
        ),
        yaxis=dict(
            autorange="reversed",
            showticklabels=True,
            title="" 
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=30, r=30, t=70, b=20),
        height=420,
        width=1700,
    )

    return fig


def main() -> None:
    fig = build_figure(SKILLS)
    out_path = os.path.join(os.getcwd(), "skill_diversity_heatmap.html")
    fig.write_html(out_path, include_plotlyjs="cdn")
    print(f"Heatmap written to: {out_path}")
    print("Open the HTML file in a browser to view the Plotly heatmap.")


if __name__ == "__main__":
    main()
