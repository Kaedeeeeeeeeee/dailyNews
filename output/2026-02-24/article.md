# カエデのAIニュース【2026年02月24日】

> 32件のニュースが到着！春の気配と共に元気にお届けします！

## 目次

1. [OpenAI Developers] gpt-realtime-1.5登場
2. [OpenAI Developers] OpenAI、APIにWebSockets導入
3. [OpenAI Developers] OpenAI、コード評価をProへ
4. [Anthropic] Anthropicへの蒸留攻撃が判明
5. [Anthropic] Anthropic、AI活用指標を発表
6. [Google] Googleが米国代表用AIツール開発
7. [Google] Google、教員600万人にGemini研修
8. [Google] GeminiにVeoテンプレート追加
9. [Google Japan] Pixel 10 Proに100倍ズーム搭載
10. [Google Gemini] GeminiにVeo 3.1テンプレート追加
11. [Google for Developers] ASにGemini 3.1 Pro搭載
12. [Google for Developers] Gemini 3.1 Pro公開
13. [Google for Developers] Geminiで3D/WebXR構築
14. [Google Antigravity] AntigravityでGPay自動実装
15. [NVIDIA] NVIDIA GB300推論性能向上
16. [NVIDIA AI Developer] NVIDIAとLMSYSが技術提携
17. [NVIDIA AI Developer] NVIDIA低精度学習1.6倍高速化
18. [AWS AI] AWSがStrands Labsを発表
19. [Microsoft Azure] ClaudeがFoundryに統合
20. [Replit ⠕] ReplitとDatabricksが連携
21. [Replit ⠕] ReplitがAI基礎講座を公開
22. [GitHub] GitHub Copilot SDKで資料作成
23. [OpenCode] AI開発のOpenCodeが連携
24. [Kilo] GLM-5がKiloで無料提供中
25. [Kilo] MiniMax 2.5活用の3D体験
26. [Hugging Face] 週刊トップAI論文リスト公開
27. [Hugging Face] RF-DETR活用監視システム
28. [Hugging Face] OlmOCR-Bench公開
29. [Kiro] KiroのAIエージェント新機能
30. [Kiro] Kiroの設計優先ワークフロー
31. [Google AI Developers] Geminiマルチモーダル関数呼出
32. [v0] v0、MCP経由でGranola連携

---

## 1. 【OpenAI Developers】gpt-realtime-1.5登場

OpenAIは、Realtime API向けの新モデル「gpt-realtime-1.5」をリリースしました。このアップデートにより、音声ワークフローの信頼性が大幅に向上します。主な改善点として、より正確な指示追従（instruction following）、ツール呼び出し（tool calling）の精度向上、そして多言語対応における正確性の強化が挙げられます。開発者はこの新モデルを利用することで、より複雑で精度の高いリアルタイム音声対話アプリケーションを構築できるようになります。

https://x.com/OpenAIDevs/status/2026014334787461508

---

## 2. 【OpenAI Developers】OpenAI、APIにWebSockets導入

OpenAIは、Responses APIにおいてWebSocketsのサポートを開始しました。この新機能は、低遅延かつ長時間稼働し、頻繁なツール呼び出しを行うAIエージェント向けに最適化されています。WebSocketsを活用することで、リアルタイム性の高いインタラクションが容易になり、複雑なタスクを実行するエージェントのパフォーマンス向上が期待できます。開発者は、応答性の高い高度なAIアプリケーションをより効率的に構築可能になります。

https://x.com/OpenAIDevs/status/2026025368650690932

---

## 3. 【OpenAI Developers】OpenAI、コード評価をProへ

OpenAIは、AIモデルの成熟に伴い、コード生成能力の評価基準を更新したことを発表しました。これまでのSWE-bench Verifiedに代わり、今後はより難易度の高い「SWE-bench Pro」の使用を推奨しています。同社は業界全体でより強固な評価基準を確立することを目指しており、モデルの進化に合わせて従来の指標を廃止し、新たな指標へと移行する詳細な理由についても共有しています。最先端モデルの性能を正確に測定するための重要な変更となります。

https://x.com/OpenAIDevs/status/2026002219909427270

---

## 4. 【Anthropic】Anthropicへの蒸留攻撃が判明

Anthropicは、DeepSeek、Moonshot AI、MiniMaxの3社が、Claudeに対して大規模な「蒸留攻撃」を行っていたことを報告しました。これらの企業は2万4,000件以上の不正アカウントを作成し、計1,600万回を超える対話を生成。Claudeの能力を抽出（蒸留）し、自社モデルの訓練や性能向上に利用していたとしています。AI開発におけるデータの安全性や、モデルの知的財産保護に関する重要な技術的課題を浮き彫りにしています。

https://x.com/AnthropicAI/status/2025997928242811253

---

## 5. 【Anthropic】Anthropic、AI活用指標を発表

Anthropicは、AIとの協働能力を測定するための新しい研究成果「The AI Fluency Index」を発表しました。Claude.aiにおける数千件の対話を分析し、プロンプトの修正や反復的な改善など、AI活用の熟練度を示す11の行動パターンを特定・追跡しています。この研究は、ユーザーがどのようにAIと協力して成果を上げているかを定量化することを目的としています。分析の結果、熟練したユーザーはAIを単なる検索ツールとしてではなく、対話を通じて思考を深めるパートナーとして活用している実態が明らかになりました。

https://x.com/AnthropicAI/status/2025950279099961854

---

## 6. 【Google】Googleが米国代表用AIツール開発

Google CloudはTeam USA（アメリカ代表チーム）の公式パートナーとして、アスリート向けのAIトレーニングツールをゼロから独自に開発したことを発表しました。このツールは、選手のパフォーマンス向上を支援するために構築されたものです。Google Cloudの先端技術をスポーツのトレーニング現場に直接導入し、データに基づいた最適化を可能にする取り組みであり、スポーツ分野における具体的なAI活用事例として注目されます。

https://x.com/Google/status/2026046882699493880

---

## 7. 【Google】Google、教員600万人にGemini研修

Googleは、米国のK-12（幼稚園から高校）の教師および高等教育機関の教職員600万人を対象に、Geminiのトレーニングプログラムの提供を開始しました。このプログラムは、多忙な教育者のニーズに合わせて設計された簡潔かつ柔軟な学習モジュールで構成されています。教育現場におけるAIの具体的な活用方法を効率的に習得できるよう支援することを目的としています。

https://x.com/Google/status/2026027188915470808

---

## 8. 【Google】GeminiにVeoテンプレート追加

Googleは、Geminiアプリにおいて動画生成モデル「Veo 3.1」のテンプレート機能を追加したことを発表しました。これにより、ユーザーは白紙のプロンプトからではなく、あらかじめ用意された高品質な視覚的基盤から動画制作を開始できるようになります。好みのスタイルを選択した後、プロンプトを使用してキャラクターや風景を重ねることで、オリジナルの動画を効率的に作成することが可能です。このアップデートは、動画生成のハードルを下げ、より直感的なクリエイティブ作業を支援することを目的としています。

https://x.com/Google/status/2026006156875804960

---

## 9. 【Google Japan】Pixel 10 Proに100倍ズーム搭載

Google Japanは、新型スマートフォン「Google Pixel 10 Pro」に搭載された100倍ズーム機能の撮影サンプルを公開しました。富士山の登山道を鮮明に記録しており、同社の強みであるAIを活用した超解像技術（Super Res Zoom）の大幅な進化が推察されます。現行モデルのスペックを上回る望遠性能の実装を示唆する、重要な製品アップデート情報です。

https://x.com/googlejapan/status/2025737373019955283

---

## 10. 【Google Gemini】GeminiにVeo 3.1テンプレート追加

Googleは、Geminiアプリにおいて動画生成モデル「Veo 3.1」の新しいテンプレートの提供を開始しました。ユーザーはアプリ内のツールメニューから「Create videos」を選択し、ギャラリー内のテンプレートから動画を作成できます。また、参照用の写真や説明文を追加することで、テンプレートをベースにした独自のカスタマイズも可能です。このアップデートにより、Geminiを通じた動画生成プロセスがより簡素化され、直感的な操作で高度な動画制作が可能になります。

https://x.com/GeminiApp/status/2026001595708866759

---

## 11. 【Google for Developers】ASにGemini 3.1 Pro搭載

Googleは、Android StudioでのAI支援機能として「Gemini 3.1 Pro」のプレビュー版を提供開始しました。開発者は自身のGemini APIキーを接続することで、エディタ内で最新モデルによるコーディング支援をテストすることが可能です。本アップデートにより、Androidアプリ開発におけるAIアシスタントの性能向上が期待されます。

https://x.com/googledevs/status/2026054463102824813

---

## 12. 【Google for Developers】Gemini 3.1 Pro公開

Google for Developersは、Gemini 3.1 Proのショーケースを公開しました。エンジニアリングの本質を単なる作業の高速化ではなく「思考の質の向上」と定義し、最新モデルがどのように開発者の思考プロセスを支援できるかを披露しています。Gemini 3.1 Proの具体的な能力が示されており、AIによる高度なエンジニアリング支援の進展が期待されます。

https://x.com/googledevs/status/2026047186195390966

---

## 13. 【Google for Developers】Geminiで3D/WebXR構築

Googleは、同社のAIモデルGeminiを活用してインタラクティブな3Dコンセプトを迅速に試作する方法を公開しました。Canvasウェブアプリ内でGeminiを使用することで、WebXR APIを用いた3D環境やインタラクティブなモデルの構築が可能になります。開発者はAIとの対話を通じて、複雑な3Dプロトタイピングのプロセスを効率化できます。具体的な実装例やガイドもあわせて提供されており、次世代のウェブ体験における開発手法を支援する内容となっています。

https://x.com/googledevs/status/2025933667508396401

---

## 14. 【Google Antigravity】AntigravityでGPay自動実装

Google Antigravityは、プロンプト一つでウェブサイトにGPayを統合できるフルスタック・オーケストレーション機能を発表しました。このツールはAngularスタックを自動検出し、必要な依存関係のインストール、フロントエンドおよびバックエンドのコード編集を自動で行います。ファイル更新後はAntigravityブラウザにより自動で処理が完了します。開発者が手動で行う複雑な実装工程を、AIへの自然言語による指示のみで完結させることが可能になります。

https://x.com/antigravity/status/2025978965983121478

---

## 15. 【NVIDIA】NVIDIA GB300推論性能向上

NVIDIAは、Blackwell Ultra GB300ラックに関する最新のベンチマーク結果を公開しました。LMSYSによる評価では、オープンソースモデルのロングコンテキスト推論において、従来のGB200と比較してレイテンシを最大1.5倍低減し、ユーザースループットを1.87倍向上させることを実証しました。この性能向上は、高度な並列処理や精度の最適化、インテリジェントな管理技術によって実現されています。大規模言語モデルの推論インフラにおける新たな基準を提示する内容となっています。

https://x.com/nvidia/status/2026019785818149122

---

## 16. 【NVIDIA AI Developer】NVIDIAとLMSYSが技術提携

NVIDIAとLMSYS（Chatbot Arenaの運営組織）は、共同執筆による技術ブログを公開し、提携を発表しました。このブログでは、大規模言語モデル（LLM）の評価基盤や推論インフラに関する技術的な深掘りが行われています。両チームの協力により、AIモデルのパフォーマンス測定や最適化における高度な知見が提供されることが期待されます。

https://x.com/NVIDIAAIDev/status/2026052022152413637

---

## 17. 【NVIDIA AI Developer】NVIDIA低精度学習1.6倍高速化

NVIDIAは、Blackwell GPUにおいてNVFP4およびMXFP8を用いた低精度トレーニング手法を発表しました。最新の研究により、BF16と同等の精度を維持しながら、スループットを最大1.6倍向上させることに成功しています。これにより、LLM（大規模言語モデル）のスケーリングにおける速度向上とコスト削減を両立します。本手法はNVIDIA NeMoライブラリを通じて提供され、より効率的なモデル開発を可能にします。

https://x.com/NVIDIAAIDev/status/2026016413006418357

---

## 18. 【AWS AI】AWSがStrands Labsを発表

AWS AIは、モデル駆動型の自律型AI（Agentic AI）の限界を押し広げる実験的なプロジェクト群「Strands Labs」を発表しました。物理システムに知的エージェントを導入する「Strands Robots」、3D物理環境で自律型ロボットを統合する「Robots Sim」、および「AI Functions」の提供を開始します。現実世界とシミュレーション環境の両面で、高度な自律型AI技術の研究と実装を加速させる取り組みです。

https://x.com/AWSAI/status/2026042129579982877

---

## 19. 【Microsoft Azure】ClaudeがFoundryに統合

Microsoft Azureは、Microsoft FoundryにおいてAnthropicのAIモデル「Claude」を活用したアプリケーション構築が可能になったことを発表しました。これに伴い、AnthropicおよびReplitと共同で、ハンズオンデモや実際のプロダクション環境での活用事例を紹介するライブイベントを実施します。この統合により、開発者はAzureのプラットフォーム上でClaudeの高度な機能を直接利用し、インテリジェントなAIサービスの開発が可能になります。

https://x.com/Azure/status/2025975193781297392

---

## 20. 【Replit ⠕】ReplitとDatabricksが連携

AIを活用した開発プラットフォームのReplitと、データ分析基盤のDatabricksが提携を発表しました。この連携により、Replitが提唱する「Vibe coding（自然言語を用いた直感的な開発）」に、Databricksが管理するエンタープライズ品質のデータを統合することが可能になります。企業データへのシームレスなアクセスを実現することで、AIエージェントを活用したソフトウェア開発の効率化と、高度なデータ活用を両立したアプリケーション構築が促進されることが期待されます。

https://x.com/Replit/status/2026033852175782325

---

## 21. 【Replit ⠕】ReplitがAI基礎講座を公開

Replitは、学習プラットフォーム「Replit Learn」にて、初のフルモジュールとなる「AI Foundations」を公開しました。このコースはAIの基礎を体系的に学ぶための教育コンテンツです。レッスン7ではエンドツーエンドでの構築プロセスを実際に体験できるなど、実践的な内容が含まれています。開発者がReplitの環境を活用しながら、AI技術の基礎から具体的な実装までをシームレスに学習できるよう設計されています。

https://x.com/Replit/status/2025768597843538430

---

## 22. 【GitHub】GitHub Copilot SDKで資料作成

GitHubは、GitHub Copilot SDKを利用してPowerPointスライドを自動生成・更新するカスタムエージェントの構築例を公開しました。このエージェントは、最新のSDKドキュメントの調査、既存スライドのスタイル解析によるデザインの統一、およびPowerPointへの直接的なコンテンツ出力が可能です。開発者はGitHub Copilot SDKを活用することで、ドキュメント作成などの定型業務を自動化する高度なAIツールを構築できます。

https://x.com/github/status/2026004273008369682

---

## 23. 【OpenCode】AI開発のOpenCodeが連携

OpenCodeとTailscaleを統合した新プロジェクト「tailcode」が発表されました。OpenCodeはAIを活用したオープンソースのコーディング環境を提供しており、Tailscaleのネットワーク技術と組み合わせることで、セキュアなリモートアクセスや共有開発環境の構築が可能になります。AI駆動のコーディング体験を安全なプライベートネットワーク上で実現する取り組みとして注目されます。

https://x.com/opencode/status/2026018252522922102

---

## 24. 【Kilo】GLM-5がKiloで無料提供中

AIプラットフォームのKiloにおいて、最新のAIモデル「GLM-5」が現在も無料で提供されていることが報告されました。GLM-5は、openclawがホストする「KiloClaw」を通じて提供されており、現在同プラットフォームで最も人気のあるモデルとなっています。ユーザーはKiloを利用することで、GLM-5の機能をコストをかけずに試用することが可能です。

https://x.com/kilocode/status/2026015840345219391

---

## 25. 【Kilo】MiniMax 2.5活用の3D体験

Kiloは、開発ツール「Kilo CLI」とAIモデル「MiniMax 2.5」を使用して構築された、インタラクティブな3Dコンテンツ「Night in Paris」を公開しました。このプロジェクトはThree.jsをベースにしており、エッフェル塔やシェーダーで制御されたセーヌ川、オービティングカメラ、ソフトシャドウ、ACESフィルムトーンマッピングなどを備えたシネマティックな視覚体験を提供します。最新のAIモデルを活用することで、高度な3Dグラフィックスの実装とインタラクションを実現した技術事例となっています。

https://x.com/kilocode/status/2025909149821714920

---

## 26. 【Hugging Face】週刊トップAI論文リスト公開

Hugging Faceが2024年2月16日から22日までの期間における週刊トップAI論文リストを公開しました。掲載された主な論文には、LLMの機能空間で多様なデータを合成する手法を提案する「Less is Enough」や、「SQuTR」などの最新の研究成果が含まれています。これらの論文は、大規模言語モデルのデータ効率化や技術的ブレークスルーを網羅しており、AI研究の最前線を知る上で重要な情報となります。

https://x.com/huggingface/status/2026011044812865932

---

## 27. 【Hugging Face】RF-DETR活用監視システム

Hugging Faceが、RoboflowのRF-DETRを用いたコンピュータビジョンによる監視システムの構築事例を共有しました。本システムはライブWebカメラの映像を利用し、物体検出モデルであるRF-DETRによってリアルタイムに状況を監視します。DETR（Detection Transformer）のリアルタイム版であるRF-DETRを活用した、具体的な物体検出の実装例となっています。

https://x.com/huggingface/status/2025988671984259333

---

## 28. 【Hugging Face】OlmOCR-Bench公開

Allen Institute for AI（Allen AI）が開発した「OlmOCR-Bench」が、Hugging Faceの公式ベンチマークデータセットとして公開されました。このベンチマークは、モデルの性能を客観的に評価・比較するためのプラットフォームです。ユーザーはYAMLファイルを追加することで、自身のモデルをこのベンチマークに登録し、評価を受けることが可能です。AIモデル、特にOCRや文書解析に関連する技術評価の新たな指標として活用が期待されます。

https://x.com/huggingface/status/2025932834091807034

---

## 29. 【Kiro】KiroのAIエージェント新機能

Kiroのプラットフォーム上で、コード作成から製品マーケティングまでを一貫して完結させる「Agent Skills」機能が紹介されました。開発者が外部のSaaSツールを利用することなく、AIエージェントを通じて製品の出荷やマーケティング活動を直接実行できるワークフローを提供します。開発プロセスの効率化を目指し、AIエージェントの実用的なスキルセットの活用に焦点を当てています。

https://x.com/kirodotdev/status/2025997479347429818

---

## 30. 【Kiro】Kiroの設計優先ワークフロー

AIを活用した仕様策定ツール「Kiro Specs」において、設計から要件を導き出す「Design-First（設計優先）」ワークフローが発表されました。従来の要件定義から設計を行う順序とは異なり、まずアーキテクチャ設計から開始することで、実現可能性が保証された要件を自動的に抽出します。これにより、設計と要件の整合性を確認するための反復的な調整プロセスを排除し、開発効率を大幅に向上させることが可能です。

https://x.com/kirodotdev/status/2025986518146240858

---

## 31. 【Google AI Developers】Geminiマルチモーダル関数呼出

Google AI Developersは、Gemini Interactions APIにおいてマルチモーダル関数呼び出し（Multimodal function calling）の提供を開始しました。これにより、開発者は画像をネイティブに認識・処理できるエージェントを構築可能になります。ツールがテキストによる説明ではなく実際の画像を返し、Gemini 3がその画像を直接処理する仕組みです。関数の実行結果としてテキストと画像が混在したデータ形式をサポートしており、より高度で視覚的な判断を伴うAIエージェントの開発が容易になります。

https://x.com/googleaidevs/status/2026008676507525243

---

## 32. 【v0】v0、MCP経由でGranola連携

Vercelが提供するAI UI生成ツール「v0」が、MCP（Model Context Protocol）を通じてAI議事録ツール「Granola」のノートをコンテキストとして利用可能になりました。これにより、会議メモの内容を直接チャットに読み込み、議論された内容を即座にプロダクションレベルの機能やUIへと変換できます。会議から開発実装までのワークフローをシームレスに繋ぐ実用的なアップデートです。

https://x.com/v0/status/2026025368210313673

---
