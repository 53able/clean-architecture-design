---
name: clean-architecture-design
description: Clean Architectureの原則で既存コードの設計診断、境界選定、段階的リファイン、依存境界レビューを支援する。Use when ユースケース中心の構造化、actor別の変更分離、port/adaptor、可変状態、テスト可能性、componentのリリース境界、循環依存、モノリスまたはサービス境界を確認または改善するとき。Don't use for 単なる命名・整形、要件根拠のない全面リライト、パフォーマンス測定だけ、フレームワーク固有APIの調査だけ。
---

# Clean Architecture 設計

## 手順

### Step 1: 対象・振る舞い・変更コストを確定する

1. 対象を、既存コードの診断、変更要求の設計、段階的リファイン、または設計レビューとして確定する。
2. `assets/actor-use-case-map-template.md` をコピーし、actor、use case、保持する振る舞い、現在のテストを記録する。
3. 主な入力、出力、外部I/O、ビルド単位、デプロイ単位、所有チームを抽出する。
4. 対象変更について、変更対象の広がり、影響を受けるcomponent/チーム、再検証範囲、調整作業を記録する。
5. use case、変更アクター、または保持する振る舞いが不明な場合は、境界や抽象化を提案する前に一つだけ確認する。

### Step 2: policy・詳細・状態を観察する

1. `references/design-rules.md` を読み、policyの分類、違反候補、反証質問を確認する。
2. 各モジュールを、ドメイン方針、アプリケーション方針、インターフェースアダプター、フレームワーク/ドライバーへ暫定分類する。
3. import、参照、継承、公開API、フレームワーク型、DBモデル、通信DTO、DI登録、テストを調べる。
4. 各モジュールについて、変更アクター、変更頻度、同時変更先、入力/出力からの距離を記録する。
5. 可変状態を列挙し、所有component、更新者、並行アクセス、排他またはトランザクション境界、復元/再試行の要否を記録する。
6. hardware、OS固有API、DB方言、専用deviceを含む場合は、platform依存、protocol解析、device driver、use caseが混在していないかを記録する。
7. フォルダ名、ファイル名、クラス数だけで分類・分割を確定しない。実際の責務と依存を証拠として記録する。

### Step 3: actor/use caseをcomponent候補へ写像する

1. `references/architecture-evaluation.md` を読み、二次元分離、componentの成立条件、可変状態の診断を確認する。
2. actorごとの変更理由でcomponent候補を分け、各候補の内部をpolicyのlevelで整理する。
3. `controller`、`presenter`、`interactor`の技術名だけでcomponentを横断分割しない。actor/use caseが同じ変更理由を共有する場合だけまとめる。
4. component候補ごとに、公開契約、依存先、ビルド単位、リリース単位、所有者、互換性条件を記録する。
5. common closure、common reuse、reuse/release equivalenceのどれを優先しているかを記録し、不要な再利用依存と不用意な分割を同時に点検する。
6. 独立した検証またはリリースの根拠がない場合は、package/moduleをdeployable componentと呼ばない。

### Step 4: 依存違反と変更結合を検査する

1. 内側から外側への依存、外部形式の内側への流入、use caseの迂回、責務混在、不要な再利用依存、循環依存を候補として抽出する。
2. リポジトリの依存グラフを抽出できる場合は、`assets/boundary-inventory.template.json` をコピーしてインベントリを作成する。
3. インベントリを作成した場合は、`/usr/bin/python3 scripts/check-boundary-inventory.py --inventory <path>` を実行する。
4. スクリプトの結果を静的なインベントリ検査として扱う。未記載の依存、実行時の結合、データ契約は別に確認する。
5. 各候補について、依存の実在、変動性、変更影響、現状維持のコストを記録する。原則名だけで違反を断定しない。

### Step 5: 境界の強さと状態境界を選ぶ

1. 新しい境界が必要な候補だけ、`references/boundary-options.md` を読む。
2. `assets/boundary-decision-template.md` をコピーし、境界なし、source-level分離、deployable component、process/serviceの四案を比較する。
3. 最も弱く安価な境界で、必要な変更・テスト・開発・デプロイの独立性を満たす案を選ぶ。
4. 可変状態を含む境界では、状態所有者を一つに定め、更新API、同時更新時の規則、排他/トランザクション、失敗後の回復を明記する。
5. serviceを選ぶ場合は、共有データ、同時デプロイ、通信失敗、観測、運用責任の追加コストを必ず記録する。
6. 完全境界、一次元境界、Facadeを区別する。Facadeを隔離の証明として扱わない。
7. 独立便益を具体的に説明できない場合は、既存の境界を維持し、提案を停止する。

### Step 6: port/adaptorとcomposition rootを設計する

1. `assets/diagnosis-template.md` をコピーし、観察と設計案を分離して記録する。
2. portを追加する場合は、利用側、高水準policyが所有する契約、実装候補、境界横断データ、test doubleを明記する。
3. use caseの入力と出力を、HTTP、ORM、DB行、SDK、フレームワーク固有型から分離する。
4. Gatewayを、SQL、ORM、汎用CRUDではなく、use caseが必要とする操作の語彙で定義する。
5. Presenterを出力モデルからview modelへの整形へ限定し、Viewをデータ転送に近づける。
6. 具体実装、設定、DI、外部資源の生成をcomposition rootへ集約し、高水準policyへ制御を渡す。
7. 安定した標準ライブラリや変更しない具体物を、原則だけを理由に抽象化しない。

### Step 7: 段階的なリファイン計画を作る

1. `references/refinement-rules.md` を読み、移行順序と停止条件を確認する。
2. `assets/migration-plan-template.md` をコピーし、use case一つに限定した最小の移行計画を作る。
3. 外側のhandler/controllerから薄い入口を抽出し、外部I/Oをportの背後へ一つずつ移す。
4. 変換をadapterへ置き、具体実装の結線をcomposition rootへ移す。
5. 依存ルール、循環依存、状態境界を検査してから、次のuse caseへ進む。
6. 変更対象が広がる、portが実装詳細を再掲する、状態所有者が曖昧になる、またはテストで振る舞いを固定できない場合は、分割を停止してStep 2へ戻る。

### Step 8: 反証して検証する

1. `references/design-rules.md` の反証質問に答え、過剰抽象化、偽の共通interface、DTOの写経、サービス分割の誤用を探す。
2. 正常系、不正入力、境界値、外部I/O失敗、並行更新、契約違反を反証候補にして、対象use caseのテスト、既存テスト、依存検査、状態境界の検査を実行する。
3. テストが失敗した場合は、設計主張、契約、境界、実装のどれを反証したか記録する。テスト成功を正しさの証明として扱わない。
4. 内側のpolicyが外部I/Oなしにテストできること、禁止依存が増えていないこと、境界横断データが詳細型を漏らしていないことを確認する。
5. 変更対象・再検証範囲・調整作業が増える案は、独立便益を再評価する。
6. 継続的な設計レビューでは、`assets/architecture-watch-template.md` をコピーし、境界の摩擦、componentの成熟度、反証結果を記録する。
7. 実行できなかった検証は、理由と影響を `未実行` または `blocked` として記録する。
8. 観察、推論、提案、未確認事項を同じ文として混ぜない。

## エラー処理

- `check-boundary-inventory.py` が `inventory_error` を返した場合は、`assets/boundary-inventory.template.json` と照合し、必須キー、層名、重複名を修正して再実行する。
- `boundary_violation` または `dependency_cycle` が出た場合は、例外として無視しない。設計意図、影響、解消案、撤去条件を記録する。
- 可変状態の所有者または同時更新規則が不明な場合は、並行化、service分割、event sourcingを提案しない。状態遷移と更新者を先に確定する。
- componentの分割がrebuild、再検証、リリース、互換性調整を増やす場合は、common closure、common reuse、release境界のどれを優先するか再評価する。
- 言語やビルド構成がモジュール可視性を強制できない場合は、静的解析、アーキテクチャテスト、ビルド単位で補完し、未強制の境界を明記する。
