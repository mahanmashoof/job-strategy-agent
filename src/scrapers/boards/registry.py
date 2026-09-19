from typing import List, Dict, Type
from src.scrapers.boards.base_board import BaseJobBoard
from src.scrapers.boards.remoteok import RemoteOKBoard
from src.scrapers.boards.wwr import WWRBoard
from src.scrapers.boards.himalayas import HimalayasBoard

# Register all available boards here
BOARDS: Dict[str, Type[BaseJobBoard]] = {
    RemoteOKBoard.name: RemoteOKBoard,
    WWRBoard.name: WWRBoard,
    HimalayasBoard.name: HimalayasBoard,

    # Add new boards here as you build them
}


def get_board(name: str) -> BaseJobBoard:
    if name not in BOARDS:
        raise ValueError(f"Unknown board: {name}. Available: {list(BOARDS.keys())}")
    return BOARDS[name]()


def list_boards() -> List[str]:
    return list(BOARDS.keys())


def fetch_all(limit_per_board: int = 100) -> List[Dict]:
    """Fetch from every registered board"""
    all_jobs = []
    for name in BOARDS:
        print(f"⏳ Fetching from {name}...")
        try:
            board = get_board(name)
            jobs = board.fetch_jobs(limit=limit_per_board)
            print(f"   ✅ {len(jobs)} jobs")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"   ❌ {name} failed: {e}")
    return all_jobs