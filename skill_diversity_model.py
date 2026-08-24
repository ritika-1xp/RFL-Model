from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass(frozen=True)
class SkillEntry:
    skill: str
    current_pct: float
    target_pct: float

    @property
    def gap_pct(self) -> float:
        return self.current_pct - self.target_pct

    @property
    def current_hours(self) -> float:
        return (self.current_pct / 100.0) * 1000.0

    @property
    def target_hours(self) -> float:
        return (self.target_pct / 100.0) * 1000.0

    @property
    def gap_hours(self) -> float:
        return self.current_hours - self.target_hours

    @property
    def heatmap_status(self) -> Tuple[str, str]:
        if abs(self.gap_pct) <= 0.75:
            return "green", "on target"
        if self.gap_pct > 0:
            return "blue", "reduce"
        return "red", "collect more"

    def to_dict(self) -> Dict[str, float | str]:
        color, action = self.heatmap_status
        return {
            "skill": self.skill,
            "current_pct": self.current_pct,
            "target_pct": self.target_pct,
            "gap_pct": self.gap_pct,
            "current_hours": round(self.current_hours, 2),
            "target_hours": round(self.target_hours, 2),
            "gap_hours": round(self.gap_hours, 2),
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


def compute_distribution_metrics(entries: List[SkillEntry], max_score: float = 10.0) -> Dict[str, float | int]:
    """Simple 0-10 model using mean absolute percentage gap from target.

    This is a transparent first-pass model for a 1000-hour dataset.
    It keeps the score tied directly to distance from target, which matches
    the heatmap interpretation you showed.
    """
    if not entries:
        return {"mean_abs_gap_pct": 0.0, "score_0_10": 0.0, "on_target": 0, "over_target": 0, "under_target": 0}

    mean_abs_gap = sum(abs(e.gap_pct) for e in entries) / len(entries)
    score = max(0.0, min(max_score, max_score * (1 - (mean_abs_gap / 20.0))))

    on_target = sum(1 for e in entries if abs(e.gap_pct) <= 0.75)
    over_target = sum(1 for e in entries if e.gap_pct > 0.75)
    under_target = sum(1 for e in entries if e.gap_pct < -0.75)

    return {
        "mean_abs_gap_pct": round(mean_abs_gap, 2),
        "score_0_10": round(score, 2),
        "on_target": on_target,
        "over_target": over_target,
        "under_target": under_target,
    }


def build_heatmap_table(entries: List[SkillEntry]) -> List[Dict[str, float | str]]:
    rows = [e.to_dict() for e in entries]
    rows.sort(key=lambda row: abs(float(row["gap_pct"])), reverse=True)
    return rows


def print_summary(entries: List[SkillEntry]) -> None:
    metrics = compute_distribution_metrics(entries)
    print("Skill Diversity Summary")
    print("=" * 80)
    print(f"Mean absolute gap from target: {metrics['mean_abs_gap_pct']}%")
    print(f"Skill Diversity Score (0-10): {metrics['score_0_10']} / 10")
    print(f"On target: {metrics['on_target']}")
    print(f"Over target: {metrics['over_target']}")
    print(f"Under target: {metrics['under_target']}")
    print()

    print("Skill | Current % | Target % | Gap % | Hours (1000h) | Status")
    print("-" * 110)
    for row in build_heatmap_table(entries):
        print(
            f"{row['skill']} | "
            f"{row['current_pct']} | "
            f"{row['target_pct']} | "
            f"{row['gap_pct']:+.1f} | "
            f"{row['current_hours']:.1f} / {row['target_hours']:.1f} | "
            f"{row['heatmap_color']} ({row['action']})"
        )


if __name__ == "__main__":
    print_summary(SKILLS)
