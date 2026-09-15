# Topic backlog

The workflow takes the first unchecked box each day and ticks it once the entry
is written. Reorder freely — whatever sits at the top goes next. Add your own;
when the list runs dry the workflow proposes a new topic instead of stopping.

## ServiceNow — platform

- [x] GlideRecord vs GlideAggregate: when the row count actually matters
- [x] Why `setWorkflow(false)` is not a performance optimisation
- [ ] Before vs after vs async business rules: the ordering that bites you
- [ ] Display business rules and the `g_scratchpad` round trip
- [ ] ACL evaluation order, and why a read ACL on a field silently wins
- [ ] `GlideRecordSecure` vs `GlideRecord`: what "secure" covers
- [ ] Scoped apps and cross-scope privileges
- [ ] Update sets: what they capture and what they quietly do not
- [ ] Table rotation and why audit tables grow the way they do
- [ ] Dictionary overrides on extended tables
- [ ] The `sys_id` as a foreign key: reference qualifiers under load
- [ ] Dynamic reference qualifiers vs advanced ones
- [ ] Domain separation: the query modifier you cannot see
- [ ] Scheduled jobs, `sys_trigger`, and duplicate execution
- [ ] Event queue vs Flow Designer triggers
- [ ] `gs.eventQueue` payload limits and how people work around them badly

## ServiceNow — Flow Designer, IntegrationHub, AI

- [ ] Flow Designer subflows: input/output contracts worth designing up front
- [ ] Error handling in flows, and the "flow succeeded, nothing happened" case
- [ ] IntegrationHub REST steps vs a scripted RESTMessageV2
- [ ] Rate limiting and retry semantics on outbound REST
- [ ] Inbound REST: scripted API vs Table API tradeoffs
- [ ] MID Server: when you actually need one
- [ ] AI Agent Studio: how tools are exposed to an agent
- [ ] Grounding an agent in CMDB data without leaking the whole table
- [ ] Predictive Intelligence: what a similarity model is really scoring
- [ ] Why classification models drift on incident data

## ServiceNow — modules

- [ ] CSM: account/contact hierarchy and entitlement resolution
- [ ] CSM: case vs incident, and the escalation path in between
- [ ] ITSM: priority from impact × urgency, and why teams override it
- [ ] ITSM: major incident workflow and the comms it triggers
- [ ] Change: CAB approvals modelled as data instead of as a process
- [ ] HRSD: lifecycle events and the fan-out problem
- [ ] HRSD: COE separation and why HR data leaks happen
- [ ] SPM: demand → project → task rollups
- [ ] SPM: resource plans and the allocation vs capacity distinction
- [ ] SLA definitions: pause conditions and the retroactive-start trap

## Applied AI / ML

- [ ] Attention is a soft lookup table — the shape walkthrough
- [ ] Why positional encodings exist, and what RoPE changed
- [ ] KV caching: the memory arithmetic
- [ ] Tokenisation surprises: numbers, whitespace, and non-Latin scripts
- [ ] Temperature vs top-p vs top-k, and picking one on purpose
- [ ] Chunking for RAG: why fixed-size splits lose the answer
- [ ] Embedding similarity is not relevance
- [ ] Hybrid retrieval: BM25 + dense, and the reranker that earns its keep
- [ ] Evaluating a RAG system without a labelled set
- [ ] LLM-as-judge: the biases you inherit
- [ ] Prompt injection in tool-using agents
- [ ] Structured output: JSON mode vs grammar-constrained decoding
- [ ] Fine-tuning vs RAG vs prompting: the actual decision boundary
- [ ] LoRA: which matrices, and why rank is small
- [ ] Quantisation: what int8 costs you and where
- [ ] Class imbalance: why accuracy hides the failure
- [ ] Precision/recall tradeoff as a business decision, with a worked example
- [ ] ROC-AUC vs PR-AUC on a rare positive
- [ ] Calibration: a confident model that is wrong
- [ ] Leakage: the five ways it enters a pipeline
- [ ] Cross-validation when rows are not independent
- [ ] Feature scaling: which models care and which do not
- [ ] Gradient boosting vs random forest, in one sentence each and a benchmark
- [ ] SHAP values: what they do and do not explain
- [ ] Time-series splits and the backtest that lies to you
- [ ] Concept drift vs data drift, and how each is detected
- [ ] Experiment tracking as a discipline, not a tool

## Engineering craft

- [ ] Idempotency keys in integrations
- [ ] Exponential backoff with jitter, and why jitter matters
- [ ] At-least-once vs exactly-once, and the lie in the middle
- [ ] Database indexes: covering, composite, and column order
- [ ] N+1 queries and how they hide behind an ORM
- [ ] Optimistic vs pessimistic locking
- [ ] UTC everywhere, and the one place it breaks
- [ ] Cron expressions: the day-of-week / day-of-month OR
- [ ] Git rebase vs merge, decided by audience
- [ ] Semantic versioning and what a breaking change actually is
- [ ] Feature flags as a deployment strategy
- [ ] Structured logging and the fields you always want
- [ ] The difference between a metric, a log, and a trace
- [ ] Error budgets and what an SLO commits you to
- [ ] Code review: the comments worth leaving
- [ ] Writing a postmortem that changes something
