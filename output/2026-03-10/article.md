# カエデのAIニュース【2026年03月10日】

> 春めく火曜日、21件もの最新AIニュースをお届けします！

## 目次

1. [OpenAI] OpenAIがPromptfooを買収
2. [OpenAI Developers] OpenAI Agents SDK自動化
3. [Claude] ClaudeにCode Review機能追加
4. [Google DeepMind] DeepMindの衛星埋め込みデータ
5. [Google] Googleの2月AI新機能まとめ
6. [Google Gemini] Gemini画像生成モデル更新
7. [Gemini CLI] Gemini CLIに最小表示モード
8. [Google Labs] Pomelliを170カ国展開
9. [Google Antigravity] Antigravity 非同期AI連携
10. [NVIDIA AI Developer] Nemotron 3 Nanoの採用拡大
11. [NVIDIA AI Developer] LLMのプライバシー保護新技術
12. [Microsoft Azure] NasdaqのAzure AI導入事例
13. [Replit ⠕] Replit Core無料キャンペーン
14. [OpenCode] MiMo V2 Flashが今週無料
15. [Zed] Zed Pro、学生に1年無料開放
16. [Visual Studio Code] VS CodeとFigmaがMCPで連携
17. [Visual Studio Code] VS Code、C++のAI支援強化
18. [Factory] Droidによるアプリ自律開発
19. [Hugging Face] HFにUlysses並列化が統合
20. [Google AI Developers] Nano Banana 2の活用事例
21. [Google AI Developers] TranslateGemma 4Bがブラウザで動作

---

## 1. 【OpenAI】OpenAIがPromptfooを買収

OpenAIは、AI評価プラットフォームを開発するPromptfooの買収を発表しました。この買収により、OpenAI Frontierにおけるエージェント型システムのセキュリティテストおよび評価機能が強化されます。Promptfooは買収後も現在のライセンスの下でオープンソースとして維持され、既存顧客へのサービス提供やサポートも継続されます。OpenAIは、高度なAIモデルの安全性と信頼性を向上させるための技術基盤を拡充する狙いです。

https://x.com/OpenAI/status/2031052793835106753

---

## 2. 【OpenAI Developers】OpenAI Agents SDK自動化

OpenAIは、Agents SDKリポジトリの保守において「skills」を用いた自動化ワークフローを導入していることを公開しました。これは検証、統合テスト、リリースチェック、PRの引き継ぎといった一連の作業を、再現可能なワークフローとして実行する仕組みです。この技術により、開発プロセスにおける品質管理やリリース作業の効率化が図られています。Agents SDKにおけるGitHubリポジトリの管理手法や、エージェントを活用した開発支援の具体例として、開発者にとって有用な技術情報となっています。

https://x.com/OpenAIDevs/status/2031059589186359524

---

## 3. 【Claude】ClaudeにCode Review機能追加

AnthropicのClaude Codeに、新機能「Code Review」が追加されました。この機能は、GitHub等でプルリクエスト（PR）が作成された際に、Claudeが複数の自律型エージェントを派遣してコード内のバグを自動的に探索するものです。開発フローにAIによる高度な検証プロセスを統合することで、ソフトウェアの品質向上とデバッグ作業の効率化を支援します。

https://x.com/claudeai/status/2031088171262554195

---

## 4. 【Google DeepMind】DeepMindの衛星埋め込みデータ

Google Earthは、Google DeepMindの基盤モデル「AlphaEarth」を活用した「Satellite Embedding dataset」を発表しました。このデータセットは、衛星画像を機械学習に適したベクトル表現（埋め込み）に変換したものです。AlphaEarthは地球観測データに特化したモデルであり、土地被覆の分類や環境モニタリングなど、多様な解析タスクの精度向上と効率化を支援します。リモートセンシング分野におけるAI活用の利便性を大きく高める、研究者や開発者向けの重要なリソースとなります。

https://x.com/GoogleDeepMind/status/2031034298665464102

---

## 5. 【Google】Googleの2月AI新機能まとめ

Googleは2月のAIアップデート内容をまとめとして公開しました。主な発表には、Pro並みの性能とFlashの速度を両立させた「Nano Banana 2」、Geminiアプリ内で利用可能な最先端の音楽生成ツール「Lyria 3」、そして問題解決において最高水準の性能を誇る「Gemini 3.1 Pro」が含まれます。これらにより、音楽生成から高度な推論まで、多様な領域におけるAI機能の拡充と性能向上が実現されています。

https://x.com/Google/status/2031075991041241104

---

## 6. 【Google Gemini】Gemini画像生成モデル更新

GoogleのGeminiアプリにおいて、画像生成モデルのアップデート「Nano Banana 2」が導入されました。この更新により、現実世界の知識の向上、高度なテキストレンダリング、画像生成用テンプレートの追加、アスペクト比の制御、およびキャラクターの再現性（Character preservation）の維持といった複数の新機能と改善が提供されます。これにより、ユーザーはより精密で柔軟な画像生成が可能になります。

https://x.com/GeminiApp/status/2031088015423189102

---

## 7. 【Gemini CLI】Gemini CLIに最小表示モード

Gemini CLIに、UIをプロンプト入力ボックスのみに簡略化する「Minimalist mode（ミニマリストモード）」が導入されました。Tabキーを2回押すことで、画面上のノイズを排除し、シンプルな表示に切り替えることが可能です。また、ツール呼び出し（tool calls）の表示を簡素化し、より合理的で冗長さを抑えた形式にするアップデートも現在開発中であることが公表されました。

https://x.com/geminicli/status/2031054595384865143

---

## 8. 【Google Labs】Pomelliを170カ国展開

Google Labsは、AIツール「Pomelli」の提供範囲を世界170以上の国と地域に拡大したことを発表しました。ユーザーからの強い要望に応える形で実施された今回のアップデートにより、これまで利用が制限されていた地域でもアクセスが可能となります。実験的なAIプロジェクトを推進するGoogle Labsにとって、このグローバル展開はユーザーベースを広げ、さらなる技術改善に向けた重要なステップとなります。

https://x.com/GoogleLabs/status/2031050796280975724

---

## 9. 【Google Antigravity】Antigravity 非同期AI連携

Googleの「Antigravity」が、非同期エージェントとの共同作業機能を発表しました。従来のようにAIの出力完了を待つ必要がなく、生成中のアーティファクトに対してリアルタイムでコメントを入れ、指示を修正することが可能です。エンジンの稼働を止めることなく、実行中のエージェントを直接誘導できる点が特徴で、人間とAIのより効率的なインタラクティブ連携を実現します。

https://x.com/antigravity/status/2031080944384311532

---

## 10. 【NVIDIA AI Developer】Nemotron 3 Nanoの採用拡大

NVIDIAは、オープンな基盤モデル「NVIDIA Nemotron 3 Nano 30B」が、OpenRouterにおいてOpenClawによる利用数で首位になったことを報告しました。このモデルは効率性に優れ、開発者はこれを用いて自律的なエージェント・システム（agentic systems）の構築を急速に進めています。軽量かつ高性能なNemotronシリーズが、実際の開発現場で重要な選択肢となっていることを示しています。

https://x.com/NVIDIAAIDev/status/2031121604076277863

---

## 11. 【NVIDIA AI Developer】LLMのプライバシー保護新技術

NVIDIAは、LLMのワークロードにおけるプライバシー保護とパフォーマンスの両立に向けた新手法を公開しました。OpenClaw、vLLM、およびProtopia AIを組み合わせ、Stochastic Embeddings（確率的埋め込み）を活用することで、機密データを保護しつつクラウド規模の効率性を維持します。この技術の最大の特徴は、ローカルでのホスティングを必要とせず、クラウド環境で安全なデータ処理を可能にする点です。これにより、セキュリティ上の制約がある環境でも、効率的なLLMの運用が期待されます。

https://x.com/NVIDIAAIDev/status/2031088884977676509

---

## 12. 【Microsoft Azure】NasdaqのAzure AI導入事例

Nasdaq Boardvantageは、取締役会ガバナンス向けAIの構築において、Azure Database for PostgreSQLを採用しました。信頼性を重視した設計により、正確でコンプライアンスに準拠したインサイトの提供を実現しています。この導入により、レビュー時間が60%短縮され、準備作業が25%削減されるなど、AIによる業務効率の大幅な向上が達成されました。

https://x.com/Azure/status/2031112794402168888

---

## 13. 【Replit ⠕】Replit Core無料キャンペーン

AI駆動型の開発プラットフォームを提供するReplitは、国際女性デーを記念した期間限定のキャンペーンを実施しています。Replit Coreを1ヶ月分ギフトとして贈ると、贈った本人も1ヶ月分が無料になる、あるいは20ドル分のクレジットを獲得できる特典を提供しています。このオファーは本日中に終了する予定で、AI機能を活用できるサブスクリプションプランをお得に利用できる機会となっています。

https://x.com/Replit/status/2030777012739326426

---

## 14. 【OpenCode】MiMo V2 Flashが今週無料

MiMo V2 Flashが今週限定で無料で提供されています。ユーザーの間では、GLM-5やK2.5などの高度な計画能力を持つモデルと、M2.5のような高速処理モデルを組み合わせて利用する手法が注目されています。今回の無料公開により、高速モデルを連携させた効率的なAIワークフローの構築がより容易になります。

https://x.com/opencode/status/2031119793202380936

---

## 15. 【Zed】Zed Pro、学生に1年無料開放

高性能コードエディタ「Zed」は、学生および教職員を対象に「Zed Pro」を1年間無料で提供する「Zed for Students」を開始しました。Proプランには、月額10ドル分のAIトークンクレジットと、AIによる無制限の編集予測機能（Edit Predictions）が含まれます。これにより、対象者は最新のAI補完機能を活用した開発環境をコストなく利用可能です。申請は公式サイトから受け付けています。

https://x.com/zeddotdev/status/2031116357325267252

---

## 16. 【Visual Studio Code】VS CodeとFigmaがMCPで連携

Visual Studio Codeは、FigmaのMCP（Model Context Protocol）サーバーが双方向のワークフローに対応したことを発表しました。これにより、Figma上のデザインをコードに取り込むだけでなく、レンダリングされたUIを編集可能なフレームとしてFigmaのキャンバスへ書き戻すことが可能になります。AIエージェントがツールを利用するための共通規格であるMCPを介することで、デザインと開発のシームレスな統合が実現します。詳細は明日午前9時30分（太平洋標準時）のライブ配信にて公開される予定です。

https://x.com/code/status/2031095720774611013

---

## 17. 【Visual Studio Code】VS Code、C++のAI支援強化

Visual Studio Codeは、C++開発者向けのAI支援機能を大幅に強化しました。新たに導入された「シンボルレベルのコンテキスト」と「CMake対応のビルドツール」により、AIエージェントがC++特有の高度な情報を直接参照できるようになります。これにより、VS Code内でのAIによるコーディング支援がより的確になり、開発効率の向上が期待されます。

https://x.com/code/status/2031034276053925997

---

## 18. 【Factory】Droidによるアプリ自律開発

Factory社が、自律型AIエージェント「Droid」を用いたアプリ開発のデモンストレーションを公開しました。「Xbox 360のUI」と映画『Her』の美学を融合させたホームオートメーションアプリを、Droidが「Mission」として自律的に構築しました。これはAIエージェントが、高度なデザイン指示を理解し、具体的なソフトウェア製品へと落とし込む実用的な能力を備えていることを証明しています。

https://x.com/FactoryAI/status/2031063733221601718

---

## 19. 【Hugging Face】HFにUlysses並列化が統合

Snowflake AI ResearchとDeepSpeedチームが開発した「Ulysses Sequence Parallelism（DeepSpeed-Ulysses）」が、Hugging Faceのエコシステムに統合されました。この技術は、大規模言語モデル（LLM）の長文コンテキスト処理を効率化するためのシーケンス並列化手法です。通信オーバーヘッドを抑えつつ、複数のGPU間で計算を分散させることで、メモリ効率の向上と計算速度の最適化を実現します。これにより、より長い入力シーケンスを扱うモデルの開発や実行が容易になります。

https://x.com/huggingface/status/2031121165079753177

---

## 20. 【Google AI Developers】Nano Banana 2の活用事例

Google AI Developersは、Nano Banana 2をゲームや手芸、趣味などの分野で活用する具体的な事例を公開しました。最新モデルが多様なクリエイティブ領域でどのように利用できるか、その応用方法をスレッド形式で紹介しています。開発者やユーザーに対し、技術の新しい可能性を提示する内容となっています。

https://x.com/googleaidevs/status/2031082592787673513

---

## 21. 【Google AI Developers】TranslateGemma 4Bがブラウザで動作

Google AI Developersは、モデル「TranslateGemma 4B」をWebGPUとTransformers.js v4を用いて、ブラウザ上で直接実行できるようになったことを発表しました。これにより、サーバーを介さず完全にオフラインでプライバシーが保護された環境にて、55言語をサポートする翻訳アプリケーションの構築が可能になります。ローカル環境での高度なAI実行を促進する重要な技術アップデートです。

https://x.com/googleaidevs/status/2031037128734376089

---
