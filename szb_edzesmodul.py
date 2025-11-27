import json
from datetime import datetime


class SZBTrainingEntry:
    def __init__(self, date, training_type, amount):
        self.date = date
        self.training_type = training_type
        self.amount = amount

    def to_dict(self):
        return {
            "date": self.date,
            "training_type": self.training_type,
            "amount": self.amount
        }

    @staticmethod
    def from_dict(data):
        return SZBTrainingEntry(
            data["date"],
            data["training_type"],
            data["amount"]
        )


def szb_load_sessions(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [SZBTrainingEntry.from_dict(d) for d in raw]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def szb_save_sessions(filename, sessions):
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in sessions], f, indent=4, ensure_ascii=False)


def szb_stats(sessions):
    if not sessions:
        return 0.0, 0
    total = sum(float(s.amount) for s in sessions)
    count = len(sessions)
    return total, count
