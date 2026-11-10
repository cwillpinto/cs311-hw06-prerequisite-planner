"""
Homework 6: The Prerequisite Planner -- verification suite.

Run: python test_planner.py
Prints the Success Token only if every check below passes.
"""

import base64
import hashlib
import random
import sys
from typing import Dict, List

from prereq_planner import has_cycle, topological_sort

ASSIGNMENT_ID = "HW06"


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def is_valid_topo_order(order: List[str], graph: Dict[str, List[str]]) -> bool:
    if order is None:
        return False
    all_nodes = set(graph.keys()) | {v for vs in graph.values() for v in vs}
    if set(order) != all_nodes or len(order) != len(all_nodes):
        return False
    position = {node: i for i, node in enumerate(order)}
    for node, deps in graph.items():
        for dep in deps:
            if position[node] >= position[dep]:
                return False
    return True


def make_random_dag(rng: random.Random, num_nodes: int, edge_prob: float) -> Dict[str, List[str]]:
    """Build a random DAG by only allowing edges from a lower-index node to a higher-index one."""
    nodes = [f"n{i}" for i in range(num_nodes)]
    graph: Dict[str, List[str]] = {n: [] for n in nodes}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if rng.random() < edge_prob:
                graph[nodes[i]].append(nodes[j])
    return graph


def main() -> int:
    failures: list = []

    print("Replaying the Part A, Question 2/3 course graph...\n")
    graph = {
        "CS115": ["CS215", "CS258"],
        "CS215": ["CS311"],
        "CS258": ["CS311"],
        "CS311": ["CS411"],
        "CS411": [],
    }
    check("has_cycle(course graph) is False (it's a valid DAG)", has_cycle(graph) is False, failures)
    order = topological_sort(graph)
    check("topological_sort returns an order satisfying every prerequisite constraint", is_valid_topo_order(order, graph), failures)

    if failures:
        print(f"\n{len(failures)} check(s) failed -- fix these first. No token issued.")
        return 1

    print("\nTesting cycle detection...\n")
    cyclic_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],  # C -> A closes the cycle
    }
    check("has_cycle detects a real 3-node cycle", has_cycle(cyclic_graph) is True, failures)
    check("topological_sort returns None for a cyclic graph", topological_sort(cyclic_graph) is None, failures)

    self_loop_graph = {"X": ["X"]}
    check("has_cycle detects a self-loop", has_cycle(self_loop_graph) is True, failures)

    disconnected_graph = {
        "A": ["B"],
        "B": [],
        "X": ["Y"],
        "Y": [],
    }
    check("has_cycle correctly handles multiple disconnected components (no false positive)", has_cycle(disconnected_graph) is False, failures)
    disc_order = topological_sort(disconnected_graph)
    check("topological_sort works across disconnected components", is_valid_topo_order(disc_order, disconnected_graph), failures)

    check("has_cycle({}) is False", has_cycle({}) is False, failures)
    check("topological_sort({}) == []", topological_sort({}) == [], failures)

    isolated_graph = {"Solo": []}
    check("topological_sort handles an isolated course with no prerequisites", topological_sort(isolated_graph) == ["Solo"], failures)

    if failures:
        print(f"\n{len(failures)} check(s) failed. No token issued.")
        return 1

    print("\nRunning randomized stress test on random DAGs...\n")
    rng = random.Random(311)
    for trial in range(20):
        num_nodes = rng.randint(2, 15)
        dag = make_random_dag(rng, num_nodes, edge_prob=0.3)
        check(f"trial {trial}: has_cycle is False on a construction-guaranteed acyclic graph", has_cycle(dag) is False, failures)
        order = topological_sort(dag)
        check(f"trial {trial}: topological_sort produces a constraint-satisfying order (n={num_nodes})", is_valid_topo_order(order, dag), failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
