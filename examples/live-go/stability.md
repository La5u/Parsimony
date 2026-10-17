# Score sensitivity: 7 models

Analysis, not a score release. Baseline `parsimony-80-20-v0.5` (net 0.8 / churn 0.2, failure cap 25), panel `live-multilang-go-v1`: 138 tasks. Scores average all tasks; an unscored task counts at the middle of its range, and comparisons also check its best and worst case (72 tasks have a point score for every model).

**Verdict.** Read the ranking with its uncertainty, not as exact positions: Claude Opus 4.6 · AMI Agent 0.7.0 ≈ Claude Sonnet 4.6 · AMI Agent 0.7.0 ≈ Claude Haiku 4.5 · AMI Agent 0.7.0 ≈ Gemini 3.6 Flash · AMI Agent 0.7.0 ≈ DeepSeek V4.1 Flash · TianxiCode 0.1.486 ≈ Gemini 3.1 Pro Preview · AMI Agent 0.7.0 ≈ Qwen3.8-27B · AMI Agent 0.7.2 (≈ marks an adjacent pair that is statistically tied or reversed by some variation).

- **No rank changes at all** under failure cap 0–50.
- **Stable under every variation and statistically separated** (0 of 6 adjacent pairs): none.
- **Statistically indistinguishable** (paired 95% CI on the difference includes 0; 6 pairs): Claude Opus 4.6 · AMI Agent 0.7.0 vs Claude Sonnet 4.6 · AMI Agent 0.7.0, Claude Sonnet 4.6 · AMI Agent 0.7.0 vs Claude Haiku 4.5 · AMI Agent 0.7.0, Claude Haiku 4.5 · AMI Agent 0.7.0 vs Gemini 3.6 Flash · AMI Agent 0.7.0, Gemini 3.6 Flash · AMI Agent 0.7.0 vs DeepSeek V4.1 Flash · TianxiCode 0.1.486, DeepSeek V4.1 Flash · TianxiCode 0.1.486 vs Gemini 3.1 Pro Preview · AMI Agent 0.7.0, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 vs Qwen3.8-27B · AMI Agent 0.7.2.
- **Midpoint rank never changes under any variation**: Claude Opus 4.6 · AMI Agent 0.7.0 (1), Claude Sonnet 4.6 · AMI Agent 0.7.0 (2), Claude Haiku 4.5 · AMI Agent 0.7.0 (3), Gemini 3.6 Flash · AMI Agent 0.7.0 (4), Qwen3.8-27B · AMI Agent 0.7.2 (7).
- Difficulty strata answer a different question and are not counted as variations; they reverse Claude Haiku 4.5 · AMI Agent 0.7.0 > Gemini 3.6 Flash · AMI Agent 0.7.0 (solved by all); DeepSeek V4.1 Flash · TianxiCode 0.1.486 > Gemini 3.1 Pro Preview · AMI Agent 0.7.0 (solved by all).

## Ranking

Rank range is the best and worst rank across all weight, cap, panel and repository variations. Bootstrap is a paired task bootstrap over all 138 tasks (2000 draws, seed 42); its 95% CI spans the resampled lower and upper bounds. Bounds treat unscored tasks at their best and worst case.

| Rank | Model | Score | 95% CI | Bounds (all tasks) | Rank range | Bootstrap rank 95% | P(top) |
|---:|---|---:|---|---|---|---|---:|
| 1 | Claude Opus 4.6 · AMI Agent 0.7.0 | 39.7 | 29.5–49.0 | 35.8–43.6 | 1–1 | 1.0–5.0 | 0.99 |
| 2 | Claude Sonnet 4.6 · AMI Agent 0.7.0 | 32.0 | 21.3–42.5 | 27.3–36.7 | 2–2 | 1.0–6.0 | 0.01 |
| 3 | Claude Haiku 4.5 · AMI Agent 0.7.0 | 29.5 | 17.5–41.3 | 23.9–35.1 | 3–3 | 1.0–6.0 | 0.00 |
| 4 | Gemini 3.6 Flash · AMI Agent 0.7.0 | 27.4 | 13.1–41.7 | 19.9–34.9 | 4–4 | 1.0–6.0 | 0.00 |
| 5 | DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.3 | 9.6–35.5 | 15.6–28.9 | 5–6 | 1.0–7.0 | 0.00 |
| 6 | Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 21.8 | 7.7–36.6 | 13.2–30.4 | 5–6 | 1.0–7.0 | 0.00 |
| 7 | Qwen3.8-27B · AMI Agent 0.7.2 | 5.7 | -2.6–13.8 | 2.3–9.0 | 7–7 | 6.0–7.0 | 0.00 |

## Adjacent pairs

| Pair | Difference | Paired 95% CI | P(a > b) | Variations that reverse it | Bounds separate |
|---|---:|---|---:|---|---|
| Claude Opus 4.6 · AMI Agent 0.7.0 > Claude Sonnet 4.6 · AMI Agent 0.7.0 | 7.69 | -8.50 to 22.76 | 0.40 | none | no |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 > Claude Haiku 4.5 · AMI Agent 0.7.0 | 2.46 | -15.31 to 20.28 | 0.02 | none | no |
| Claude Haiku 4.5 · AMI Agent 0.7.0 > Gemini 3.6 Flash · AMI Agent 0.7.0 | 2.16 | -19.92 to 23.00 | 0.00 | none | no |
| Gemini 3.6 Flash · AMI Agent 0.7.0 > DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 5.09 | -18.09 to 28.26 | 0.03 | none | no |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 > Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 0.48 | -23.28 to 23.74 | 0.00 | net weight=0.5, net weight=0.6, net weight=0.7, panel without Gemini 3.6 Flash · AMI Agent 0.7.0, without caddyserver/caddy, without dlvhdr/gh-dash, without google/go-github, without influxdata/telegraf, without kedacore/keda, without kubernetes/kops, without kumahq/kuma, without lima-vm/lima, without oauth2-proxy/oauth2-proxy, without openfga/openfga, without twpayne/chezmoi | no |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 > Qwen3.8-27B · AMI Agent 0.7.2 | 16.11 | -2.32 to 34.99 | 0.91 | none | yes |

## Weights and failure cap

Bound-midpoint score over all tasks; rank in parentheses.

| Model | `baseline` | `net_weight=0.5` | `net_weight=0.6` | `net_weight=0.7` | `net_weight=0.9` | `net_weight=1` | `net_floor=0` | `failure_cap=0` | `failure_cap=10` | `failure_cap=50` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 39.7 (1) | 39.9 (1) | 39.8 (1) | 39.7 (1) | 39.6 (1) | 39.6 (1) | 39.6 (1) | 42.5 (1) | 41.4 (1) | 36.9 (1) |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 | 32.0 (2) | 32.5 (2) | 32.3 (2) | 32.2 (2) | 31.8 (2) | 31.7 (2) | 32.3 (2) | 35.3 (2) | 34.0 (2) | 28.7 (2) |
| Claude Haiku 4.5 · AMI Agent 0.7.0 | 29.5 (3) | 30.4 (3) | 30.1 (3) | 29.8 (3) | 29.2 (3) | 29.0 (3) | 29.9 (3) | 33.4 (3) | 31.9 (3) | 25.6 (3) |
| Gemini 3.6 Flash · AMI Agent 0.7.0 | 27.4 (4) | 26.1 (4) | 26.5 (4) | 26.9 (4) | 27.8 (4) | 28.2 (4) | 27.2 (4) | 31.9 (4) | 30.1 (4) | 22.8 (4) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.3 (5) | 19.8 (6) | 20.7 (6) | 21.5 (6) | 23.1 (5) | 23.9 (5) | 21.7 (5) | 26.7 (5) | 24.9 (5) | 17.9 (5) |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 21.8 (6) | 21.3 (5) | 21.5 (5) | 21.6 (5) | 22.0 (6) | 22.1 (6) | 21.4 (6) | 26.5 (6) | 24.6 (6) | 17.1 (6) |
| Qwen3.8-27B · AMI Agent 0.7.2 | 5.7 (7) | 5.3 (7) | 5.4 (7) | 5.6 (7) | 5.8 (7) | 6.0 (7) | 5.6 (7) | 12.9 (7) | 10.0 (7) | -1.5 (7) |

## Panel composition

Each panel model's references removed in turn (every model still scored); tasks that lose their reference remain in the full population with bounds. The dedup panel counts byte-identical patches once per task (52 of 445 references removed).

| Panel without | References removed | Tasks orphaned | Ranking changes vs baseline |
|---|---:|---:|---|
| Claude Haiku 4.5 · AMI Agent 0.7.0 | 82 | 27 | none |
| Claude Opus 4.6 · AMI Agent 0.7.0 | 97 | 29 | none |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 | 91 | 27 | none |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 64 | 25 | none |
| Gemini 3.6 Flash · AMI Agent 0.7.0 | 72 | 26 | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| Qwen3.8-27B · AMI Agent 0.7.2 | 39 | 27 | none |
| (dedup panel) | 52 | 0 | none |

Tasks that lose their only reference: Claude Haiku 4.5 · AMI Agent 0.7.0: `casbin__casbin-1512`, `casbin__casbin-1522`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-26074`, `github__gh-aw-27242`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-46272`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`; Claude Opus 4.6 · AMI Agent 0.7.0: `casbin__casbin-1512`, `casbin__casbin-1522`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-27242`, `go-vikunja__vikunja-2574`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `kubernetes__kops-17519`, `kubernetes__kops-18146`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `netbirdio__netbird-3970`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`; Claude Sonnet 4.6 · AMI Agent 0.7.0: `casbin__casbin-1512`, `casbin__casbin-1522`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-27242`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `kubernetes__kops-18152`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-42164`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`; Gemini 3.1 Pro Preview · AMI Agent 0.7.0: `casbin__casbin-1512`, `casbin__casbin-1522`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-27242`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`; Gemini 3.6 Flash · AMI Agent 0.7.0: `casbin__casbin-1512`, `casbin__casbin-1522`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23146`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-27242`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`; Qwen3.8-27B · AMI Agent 0.7.2: `cadence-workflow__cadence-7182`, `casbin__casbin-1512`, `casbin__casbin-1522`, `coder__coder-19201`, `fortio__fortio-1081`, `github__gh-aw-22943`, `github__gh-aw-23348`, `github__gh-aw-23870`, `github__gh-aw-24043`, `github__gh-aw-24521`, `github__gh-aw-27242`, `influxdata__telegraf-18556`, `influxdata__telegraf-18686`, `karmada-io__karmada-7365`, `kedacore__keda-6901`, `knative__eventing-8611`, `kubernetes-sigs__kueue-8597`, `libp2p__go-libp2p-3306`, `lima-vm__lima-3812`, `moby__moby-50281`, `nats-io__nats-server-7175`, `nginx__kubernetes-ingress-8119`, `open-telemetry__opentelemetry-collector-contrib-47408`, `open-telemetry__opentelemetry-go-contrib-7607`, `open-telemetry__opentelemetry-operator-4118`, `prometheus__alertmanager-4478`, `terraform-docs__terraform-docs-901`.

## Task mix

Leave one repository out (task count in parentheses):

| Without | Ranking changes vs baseline |
|---|---|
| 0xERR0R/blocky (1) | none |
| Gentleman-Programming/gentle-ai (1) | none |
| IBM/sarama (1) | none |
| NVIDIA/gpu-operator (1) | none |
| TecharoHQ/anubis (1) | none |
| a-h/templ (1) | none |
| akuity/kargo (2) | none |
| amir20/dozzle (1) | none |
| argoproj/argo-rollouts (1) | none |
| bpg/terraform-provider-proxmox (1) | none |
| caddyserver/caddy (2) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| cadence-workflow/cadence (1) | none |
| casbin/casbin (2) | none |
| centrifugal/centrifugo (1) | none |
| cert-manager/cert-manager (1) | none |
| charmbracelet/crush (1) | none |
| chenhg5/cc-connect (2) | none |
| coder/coder (1) | none |
| coze-dev/coze-loop (1) | none |
| crowdsecurity/crowdsec (1) | none |
| cucumber/godog (1) | none |
| danielmiessler/Fabric (1) | none |
| dlvhdr/gh-dash (1) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| envoyproxy/gateway (2) | none |
| ethereum/go-ethereum (1) | none |
| evcc-io/evcc (1) | none |
| fortio/fortio (1) | none |
| gastownhall/beads (1) | none |
| getgauge/gauge (1) | none |
| github/gh-aw (9) | none |
| github/github-mcp-server (1) | none |
| go-task/task (1) | none |
| go-vikunja/vikunja (1) | none |
| gohugoio/hugo (7) | none |
| golang-jwt/jwt (1) | none |
| google/go-github (1) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| google/starlark-go (1) | none |
| graphql-go/graphql (1) | none |
| gruntwork-io/cloud-nuke (1) | none |
| influxdata/telegraf (3) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| istio/istio (1) | none |
| jesseduffield/lazygit (1) | none |
| karmada-io/karmada (1) | none |
| kedacore/keda (3) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| knative/eventing (1) | none |
| kube-vip/kube-vip (1) | none |
| kubernetes-sigs/controller-runtime (2) | none |
| kubernetes-sigs/kubebuilder (1) | none |
| kubernetes-sigs/kueue (3) | none |
| kubernetes/kops (3) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| kubernetes/kube-state-metrics (1) | none |
| kumahq/kuma (1) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| kyverno/kyverno (2) | none |
| libp2p/go-libp2p (1) | none |
| lima-vm/lima (3) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| magefile/mage (1) | none |
| mgechev/revive (1) | none |
| moby/moby (1) | none |
| modelcontextprotocol/go-sdk (1) | none |
| modelcontextprotocol/registry (1) | none |
| moonD4rk/HackBrowserData (1) | none |
| nats-io/nats-server (2) | none |
| netbirdio/netbird (1) | none |
| nextlevelbuilder/goclaw (1) | none |
| nginx/kubernetes-ingress (1) | none |
| oauth2-proxy/oauth2-proxy (2) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| ollama/ollama (1) | none |
| open-telemetry/opentelemetry-collector-contrib (5) | none |
| open-telemetry/opentelemetry-ebpf-profiler (1) | none |
| open-telemetry/opentelemetry-go (3) | none |
| open-telemetry/opentelemetry-go-contrib (1) | none |
| open-telemetry/opentelemetry-operator (2) | none |
| openfga/openfga (1) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| ossf/scorecard (1) | none |
| pelletier/go-toml (1) | none |
| prometheus/alertmanager (1) | none |
| redpanda-data/connect (1) | none |
| rook/rook (2) | none |
| rqlite/rqlite (3) | none |
| slack-go/slack (1) | none |
| sqlc-dev/sqlc (1) | none |
| stripe/stripe-cli (1) | none |
| submariner-io/submariner (1) | none |
| sustainable-computing-io/kepler (1) | none |
| terraform-docs/terraform-docs (1) | none |
| tikv/pd (2) | none |
| tmc/langchaingo (1) | none |
| twpayne/chezmoi (3) | DeepSeek V4.1 Flash · TianxiCode 0.1.486 5→6, Gemini 3.1 Pro Preview · AMI Agent 0.7.0 6→5 |
| velero-io/velero (1) | none |
| vmware-tanzu/velero (1) | none |
| yuin/gopher-lua (1) | none |
| zitadel/zitadel (1) | none |

Difficulty strata. On tasks every model solved the score is pure footprint; on the rest it mixes correctness and footprint.

| Model | All tasks (138) | Solved by every model (17) | Solved by fewer (121) |
|---|---:|---:|---:|
| Claude Opus 4.6 · AMI Agent 0.7.0 | 39.7 (1) | 55.8 (1) | 37.4 (1) |
| Claude Sonnet 4.6 · AMI Agent 0.7.0 | 32.0 (2) | 49.5 (4) | 29.5 (2) |
| Claude Haiku 4.5 · AMI Agent 0.7.0 | 29.5 (3) | 43.5 (7) | 27.6 (3) |
| Gemini 3.6 Flash · AMI Agent 0.7.0 | 27.4 (4) | 53.5 (3) | 23.7 (4) |
| DeepSeek V4.1 Flash · TianxiCode 0.1.486 | 22.3 (5) | 49.2 (5) | 18.5 (5) |
| Gemini 3.1 Pro Preview · AMI Agent 0.7.0 | 21.8 (6) | 55.5 (2) | 17.1 (6) |
| Qwen3.8-27B · AMI Agent 0.7.2 | 5.7 (7) | 45.1 (6) | 0.2 (7) |

## What drives each adjacent gap

Diagnostic on tasks where both models have calibrated point scores, split by outcome (a/b). Contributions sum to that common-point-task gap, not the full-population bound-midpoint difference.

- **Claude Opus 4.6 · AMI Agent 0.7.0 − Claude Sonnet 4.6 · AMI Agent 0.7.0 = 9.79**: failed/failed 0.05 (8), failed/solved -3.73 (6), solved/failed 6.43 (11), solved/solved 7.03 (85). For Claude Opus 4.6 · AMI Agent 0.7.0: `go-task__task-2716` +0.83 (solved/failed), `caddyserver__caddy-7189` +0.73 (solved/failed), `rook__rook-16087` +0.69 (solved/failed). For Claude Sonnet 4.6 · AMI Agent 0.7.0: `nats-io__nats-server-7089` -0.93 (failed/solved), `gohugoio__hugo-14657` -0.75 (solved/solved), `gohugoio__hugo-14741` -0.62 (failed/solved).
- **Claude Sonnet 4.6 · AMI Agent 0.7.0 − Claude Haiku 4.5 · AMI Agent 0.7.0 = -1.87**: failed/failed 0.01 (7), failed/solved -6.84 (10), solved/failed 5.92 (10), solved/solved -0.96 (71). For Claude Sonnet 4.6 · AMI Agent 0.7.0: `nats-io__nats-server-7089` +0.93 (solved/failed), `jesseduffield__lazygit-4750` +0.82 (solved/failed), `kubernetes-sigs__controller-runtime-3247` +0.74 (solved/failed). For Claude Haiku 4.5 · AMI Agent 0.7.0: `go-task__task-2716` -0.93 (failed/solved), `istio__istio-56962` -0.89 (failed/solved), `bpg__terraform-provider-proxmox-2122` -0.81 (solved/solved).
- **Claude Haiku 4.5 · AMI Agent 0.7.0 − Gemini 3.6 Flash · AMI Agent 0.7.0 = 7.48**: failed/failed 0.02 (8), failed/solved -4.87 (9), solved/failed 12.72 (21), solved/solved -0.39 (59). For Claude Haiku 4.5 · AMI Agent 0.7.0: `open-telemetry__opentelemetry-collector-contrib-40522` +1.06 (solved/failed), `slack-go__slack-1471` +1.02 (solved/failed), `rqlite__rqlite-2190` +0.96 (solved/failed). For Gemini 3.6 Flash · AMI Agent 0.7.0: `a-h__templ-1213` -0.86 (failed/solved), `open-telemetry__opentelemetry-ebpf-profiler-734` -0.82 (failed/solved), `mgechev__revive-1686` -0.82 (solved/solved).
- **Gemini 3.6 Flash · AMI Agent 0.7.0 − DeepSeek V4.1 Flash · TianxiCode 0.1.486 = 1.71**: failed/failed 0.46 (6), failed/solved -13.14 (20), solved/failed 8.52 (11), solved/solved 5.86 (53). For Gemini 3.6 Flash · AMI Agent 0.7.0: `modelcontextprotocol__registry-321` +1.22 (solved/failed), `gohugoio__hugo-14685` +0.99 (solved/failed), `gruntwork-io__cloud-nuke-1085` +0.99 (solved/solved). For DeepSeek V4.1 Flash · TianxiCode 0.1.486: `kubernetes__kops-17519` -1.25 (failed/solved), `kubernetes__kops-18146` -1.21 (failed/solved), `kubernetes__kops-18152` -1.18 (failed/solved).
- **DeepSeek V4.1 Flash · TianxiCode 0.1.486 − Gemini 3.1 Pro Preview · AMI Agent 0.7.0 = 4.99**: failed/failed -0.53 (6), failed/solved -6.25 (8), solved/failed 13.99 (23), solved/solved -2.22 (49). For DeepSeek V4.1 Flash · TianxiCode 0.1.486: `kubernetes__kops-17519` +1.29 (solved/failed), `kubernetes__kops-18152` +1.22 (solved/failed), `kubernetes__kops-18146` +1.18 (solved/failed). For Gemini 3.1 Pro Preview · AMI Agent 0.7.0: `rqlite__rqlite-2182` -1.20 (failed/solved), `kubernetes-sigs__kueue-9866` -1.06 (solved/solved), `gohugoio__hugo-14657` -1.05 (failed/solved).
- **Gemini 3.1 Pro Preview · AMI Agent 0.7.0 − Qwen3.8-27B · AMI Agent 0.7.2 = 17.16**: failed/failed 0.36 (28), failed/solved -2.31 (4), solved/failed 16.42 (32), solved/solved 2.69 (28). For Gemini 3.1 Pro Preview · AMI Agent 0.7.0: `Gentleman-Programming__gentle-ai-50` +1.11 (solved/failed), `kubernetes-sigs__controller-runtime-3494` +0.93 (solved/failed), `rook__rook-16087` +0.85 (solved/failed). For Qwen3.8-27B · AMI Agent 0.7.2: `google__go-github-3653` -0.74 (failed/solved), `modelcontextprotocol__go-sdk-862` -0.68 (solved/solved), `google__starlark-go-599` -0.63 (solved/solved).

## Regenerate

```sh
python -m parsimony.stability examples/live-go/score-panel.json examples/live-go/claude-haiku-4.5-ami.jsonl examples/live-go/claude-opus-4.6-ami.jsonl examples/live-go/claude-sonnet-4.6-ami.jsonl examples/live-go/gemini-3.1-pro-preview-ami.jsonl examples/live-go/gemini-3.6-flash-ami.jsonl examples/live-go/qwen3.8-27b-ami-0.7.2.jsonl examples/live-go/deepseek-v4.1-flash-tianxicode-0.1.486.jsonl --output examples/live-go/stability.json
```

All numbers are in [stability.json](stability.json). The analysis is conditional on this cohort and task population; the panel is built from the same models it ranks.
