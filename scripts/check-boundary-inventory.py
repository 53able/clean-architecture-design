#!/usr/bin/env python3
"""Check a language-neutral Clean Architecture dependency inventory."""

import argparse
import json
import sys
from pathlib import Path

LAYERS = {
    "domain-policy": 0,
    "application-policy": 1,
    "interface-adapter": 2,
    "framework-driver": 3,
}


def fail(message: str) -> None:
    print(f"inventory_error: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_inventory(path: Path) -> tuple[dict[str, str], list[tuple[str, str]]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"'{path}' が見つかりません。--inventory に既存のJSONファイルを指定してください。")
    except json.JSONDecodeError as error:
        fail(f"'{path}' は有効なJSONではありません: line {error.lineno}, column {error.colno}。")

    if not isinstance(data, dict):
        fail("JSONの最上位は object にしてください。")
    components = data.get("components")
    dependencies = data.get("dependencies")
    if not isinstance(components, list) or not isinstance(dependencies, list):
        fail("'components' と 'dependencies' を配列として指定してください。")

    names: dict[str, str] = {}
    for index, component in enumerate(components):
        if not isinstance(component, dict):
            fail(f"components[{index}] は object にしてください。")
        name = component.get("name")
        layer = component.get("layer")
        if not isinstance(name, str) or not name:
            fail(f"components[{index}].name は空でない文字列にしてください。")
        if name in names:
            fail(f"component name '{name}' が重複しています。")
        if layer not in LAYERS:
            fail(
                f"components[{index}].layer は {', '.join(LAYERS)} のいずれかにしてください。"
            )
        names[name] = layer

    edges: list[tuple[str, str]] = []
    for index, dependency in enumerate(dependencies):
        if not isinstance(dependency, dict):
            fail(f"dependencies[{index}] は object にしてください。")
        source = dependency.get("from")
        target = dependency.get("to")
        if source not in names or target not in names:
            fail(f"dependencies[{index}] の from/to は components に存在する name を指定してください。")
        edges.append((source, target))
    return names, edges


def find_cycles(nodes: dict[str, str], edges: list[tuple[str, str]]) -> list[list[str]]:
    adjacency = {name: [] for name in nodes}
    for source, target in edges:
        adjacency[source].append(target)

    state = {name: 0 for name in nodes}
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for neighbor in adjacency[node]:
            if state[neighbor] == 0:
                visit(neighbor)
            elif state[neighbor] == 1:
                start = stack.index(neighbor)
                cycle = stack[start:] + [neighbor]
                if cycle not in cycles:
                    cycles.append(cycle)
        stack.pop()
        state[node] = 2

    for node in nodes:
        if state[node] == 0:
            visit(node)
    return cycles


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean Architectureの依存方向と循環をインベントリから検査する。"
    )
    parser.add_argument("--inventory", required=True, type=Path, help="検査するJSONインベントリ")
    args = parser.parse_args()

    components, dependencies = load_inventory(args.inventory)
    violations = [
        (source, target)
        for source, target in dependencies
        if LAYERS[components[source]] < LAYERS[components[target]]
    ]
    cycles = find_cycles(components, dependencies)

    if violations:
        for source, target in violations:
            print(
                "boundary_violation: "
                f"{source} ({components[source]}) -> {target} ({components[target]}) は内側から外側への依存です。",
                file=sys.stderr,
            )
    if cycles:
        for cycle in cycles:
            print(f"dependency_cycle: {' -> '.join(cycle)}", file=sys.stderr)

    if violations or cycles:
        raise SystemExit(1)
    print(
        f"OK: {len(components)} components と {len(dependencies)} dependencies に、"
        "依存方向違反と循環依存はありません。"
    )


if __name__ == "__main__":
    main()
