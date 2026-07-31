#!/usr/bin/env python3
"""
AI Everything — main entry point.

Usage:
    python3 main.py --demo
    python3 main.py --knowledge
    python3 main.py --sim
"""

import sys
from pathlib import Path

# Ensure local package is importable
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.runtime import Runtime, demo as runtime_demo
from agents.knowledge_agent import KnowledgeAgent
from agents.simulator_agent import SimulatorAgent
from core.agent import Agent
from tools.composer import ToolComposer, Tool
import json


def knowledge_demo():
    print("=" * 60)
    print("KnowledgeAgent + Ternary Search Tree Demo")
    print("=" * 60)
    ka = KnowledgeAgent()
    for _ in range(8):
        ka.tick()
    print("Facts stored:", list(ka.state.memory.keys()))
    print("Prefix 'ai':", ka.prefix_search("ai"))
    print("Exact 'provide air eat win talk':", ka.search_fact("provide air eat win talk"))
    print(json.dumps(ka.report(), indent=2, default=str))


def sim_demo():
    print("=" * 60)
    print("SimulatorAgent — Conceptual Ballistic Monte-Carlo")
    print("=" * 60)
    sa = SimulatorAgent()
    for _ in range(6):
        sa.tick()
    print("Trajectories generated:", len(sa.trajectories))
    if sa.trajectories:
        print("Example final range:", sa.trajectories[0][-1, 0])
    print(json.dumps(sa.report(), indent=2, default=str))


def composer_demo():
    print("=" * 60)
    print("ToolComposer Demo")
    print("=" * 60)
    tc = ToolComposer()

    def sysinfo(results):
        import platform
        return {"python": platform.python_version(), "machine": platform.machine()}

    def greet(results):
        return f"Hello from AI Everything (python {results.get('sysinfo', {}).get('python')})"

    def report(results):
        return {"greeting": results.get("greet"), "sys": results.get("sysinfo")}

    tc.register(Tool("sysinfo", triggers=["system", "info", "python"], fn=sysinfo))
    tc.register(Tool("greet", triggers=["hello", "greet"], requires=["sysinfo"], fn=greet))
    tc.register(Tool("report", triggers=["report", "summary"], requires=["greet", "sysinfo"], fn=report))

    out = tc.execute("give me a system report and a greeting")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Full multi-agent subsumption demo")
    parser.add_argument("--knowledge", action="store_true")
    parser.add_argument("--sim", action="store_true")
    parser.add_argument("--composer", action="store_true")
    args = parser.parse_args()

    if args.demo:
        runtime_demo()
    elif args.knowledge:
        knowledge_demo()
    elif args.sim:
        sim_demo()
    elif args.composer:
        composer_demo()
    else:
        print("AI Everything ready. Try:")
        print("  python3 main.py --demo")
        print("  python3 main.py --knowledge")
        print("  python3 main.py --sim")
        print("  python3 main.py --composer")
