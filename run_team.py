"""Run the agent team (Lab 04).

    python run_team.py TICKER --peers PEER1,PEER2 --price P     # full run: steps, roles, manager, verifier
    python run_team.py --verify-only runs/<saved run folder>     # the Verifier alone, on a saved run

Each run gets its own folder in runs/, named by company, date and time; earlier runs are never touched.
"""
import argparse

from dotenv import load_dotenv

load_dotenv()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--peers", default="")
    ap.add_argument("--price", type=float, default=None)
    ap.add_argument("--verify-only", metavar="RUN_FOLDER", default=None)
    a = ap.parse_args()

    if a.verify_only:
        from agent_team.verifier import verify
        verify(a.verify_only)
        return
    if not a.ticker:
        ap.error("give a ticker, or --verify-only RUN_FOLDER")
    from agent_team.graph import build_graph
    peers = [p.strip().upper() for p in a.peers.split(",") if p.strip()]
    final = build_graph().invoke({"ticker": a.ticker.upper(), "peers": peers, "price": a.price})
    print(f"RUN FOLDER: {final['run_folder']}")


if __name__ == "__main__":
    main()
