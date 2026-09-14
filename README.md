# Clean Architecture Design

Clean Architectureの原則を使い、既存コードの設計診断、境界選定、段階的リファイン、依存境界レビューを行うエージェントスキルです。

## インストール

```bash
npx skills add 53able/clean-architecture-design
```

## できること

- actorとuse caseを起点に、変更理由とpolicyのlevelを整理する
- 内側から外側への依存、循環依存、外部詳細の流入を検査する
- source-level分離、deployable component、process/serviceを比較し、必要最小の境界を選ぶ
- port/adaptorとcomposition rootを設計する
- 可変状態の所有、並行更新、回復規則を境界として検討する
- 一つのuse caseから安全に段階的リファインする
- 反例を探すテストで設計主張と境界を検証する

## 利用例

```text
このリポジトリの注文処理を診断し、Clean Architectureの観点から最小の改善案を作成して。
```

```text
このHTTP handlerからDBへの直接アクセスを、port/adaptorで段階的に分離する計画を作って。
```

## 読む順番

- [なぜこのスキルが必要か](docs/why-clean-architecture-design.md): 変更コストと境界選定を中心に、このスキルの目的を説明します。
- [診断から段階的リファインまで](docs/diagnosis-to-refinement.md): 観察、最小境界、port/adaptor、検証までの進め方です。
- [境界を作らない判断](docs/when-not-to-use.md): 過剰な抽象化や安易なservice分割を避ける基準です。

## 構成

- `SKILL.md`: 実行手順
- `assets/`: 診断、境界決定、移行計画、再評価のテンプレート
- `references/`: 設計・境界・段階的リファインの規則
- `scripts/`: 依存方向と循環依存を検査するスクリプト

## ライセンス

[MIT License](LICENSE)
