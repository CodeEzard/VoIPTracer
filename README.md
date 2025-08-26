# Here’s a **straight, step-by-step plan** you can execute today, from raw logs to multiparty VoIP groups with ASN/ISP mapping and (optionally) a streaming API.

---

# 0) Prep

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas networkx fastapi uvicorn pydantic geoip2
# Optional, for speed on big data: pip install polars
# Optional ASN DB (free): set GEOIP2_ASN_DB=/path/to/GeoLite2-ASN.mmdb
```

**Repo skeleton**

```
project/
	data/{cdr.csv, ipdr.csv}
	cfg/rules.yaml
	src/
		schemas.py
		load.py
		enrich.py
		heuristics.py
		correlate.py
		graph.py
		cli.py
		api.py   # optional streaming
```

---

# 1) Define data contracts (schemas)

**CDR (csv/json)**

* `subscriber: str`
* `called: str`
* `call_type: str`   (VOICE/SMS/etc.)
* `start_time: ISO8601`
* `end_time: ISO8601`

**IPDR (csv/json)**

* `subscriber: str`
* `destination_ip: str`
* `protocol: str`    (TCP/UDP)
* `dst_port: int`
* `start_time: ISO8601`
* `end_time: ISO8601`

**Acceptance check:** rows parse, times valid, `end_time ≥ start_time`.

---

# 2) Load & validate

* Implement `src/schemas.py` with Pydantic models `CDR`, `IPDR`.
* Implement `src/load.py`:

	* `load_cdr(path) -> pd.DataFrame`
	* `load_ipdr(path) -> pd.DataFrame`
	* Parse dates; drop bad rows; log counts.

**Acceptance check:** `print(df.info())` shows correct dtypes; no NaTs.

---

# 3) VoIP heuristics (metadata-only)

Create `src/heuristics.py` with:

* `is_voip_row(row) -> str|None` returning one of:

	* `"SIP-Signaling"` if `dst_port == 5060 or 5061`
	* `"RTP-Media"` if `16384 ≤ dst_port ≤ 32767`
	* `"App-VoIP-443"` if `dst_port == 443 and protocol in {UDP,TCP}` (OTT tunneling)
* Read optional allow/deny lists from `cfg/rules.yaml` (custom ports/IPs).

**Acceptance check:** run on sample and see expected flags.

---

# 4) ASN/ISP enrichment

Create `src/enrich.py`:

* `enrich_asn(df_ipdr) -> df_ipdr_enriched`
	Uses `geoip2` and `GEOIP2_ASN_DB` to add:

	* `asn: int`
	* `as_org: str`

**Acceptance check:** % rows with ASN > 0; log misses.

---

# 5) Time-overlap correlation (CDR ↔ IPDR)

Create `src/correlate.py`:

* For each subscriber, **interval-join** their CDRs to IPDRs:

	* Overlap rule: `not (ipdr.end ≤ cdr.start or cdr.end ≤ ipdr.start)`
	* Output columns:

		* `subscriber, called, call_type, cdr_start, cdr_end`
		* `destination_ip, protocol, dst_port, ipdr_start, ipdr_end`
		* `voip_flag, asn, as_org`
* Optimize:

	* Pre-group by `subscriber`.
	* Sort by `start_time` and two-pointer sweep for O(n).

**Acceptance check:** count of correlated pairs > 0; spot-check durations roughly align.

---

# 6) Build the session graph (windowed)

Create `src/graph.py`:

* **Window**: choose `W = 5m` (configurable).
* For each window:

	* Nodes: `S:subscriber`, `I:destination_ip`, `A:asn`.
	* Edges:

		* `S —(uses)→ I` if correlated row within window and `voip_flag != None`.
		* `I —(belongs_to)→ A` if ASN known.
	* Edge weight = `w1*duration_overlap + w2*heuristic_score`.
* Compute **connected components**; extract groups with `≥2` subscribers.

**Acceptance check:** groups list like:

```
[ {window: "10:00–10:05", ip: "203.0.113.5", as_org: "Google", subscribers: ["A1","B1"]}, ... ]
```

---

# 7) Multiparty detection & scoring

* For each component:

	* `members = subscribers in component`
	* `size >= 2` → multiparty candidate
	* Score = `avg(edge_weight)` or simple:

		* +2 if SIP present
		* +1 if RTP present
		* +1 if OTT-443 and AS in known-VoIP list
		* +1 if |duration(cdr) − duration(ipdr)| ≤ 60s
* Sort groups by score desc, then size desc.

**Acceptance check:** top groups align with your expectations.

---

# 8) Batch CLI (one command)

Create `src/cli.py` to run the whole pipeline:

```bash
python -m src.cli \
	--cdr data/cdr.csv \
	--ipdr data/ipdr.csv \
	--window "5min" \
	--out results/groups.jsonl
```

**CLI outputs**

* `results/correlated.parquet`
* `results/groups.jsonl` (one JSON object per windowed cluster)

**Acceptance check:** files created; non-empty.

---

# 9) Optional: Streaming API (FastAPI + WebSocket)

* `src/api.py`:

	* `POST /ingest/cdr`, `POST /ingest/ipdr` (batch JSON)
	* ASN enrichment + heuristics on ingest
	* Keep a sliding in-memory window (e.g., 15m)
	* Recompute groups; push to `/ws` as live JSON

**Run**

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8080
```

**Acceptance check:** connect to `ws://localhost:8080/ws` and see `hello`, `heartbeat`, and updates after ingest.

---

# 10) Verification (ground truth & QA)

* **Unit tests:** overlap logic, heuristic labels, ASN lookup stub.
* **Golden dataset:** a few synthetic sessions:

	* SIP→RTP pair → must cluster
	* Two subs to same OTT IP:443 at same time → must cluster
	* Non-overlapping sessions → must NOT cluster
* **Metrics:** log precision/recall if you have labeled truth; otherwise log:

	* `% ipdr flagged voip`
	* `% ipdr with asn resolved`
	* `groups/hour`, top `as_org` by groups

---

# 11) Scale & hardening (as needed)

* Swap `pandas` for **Polars** or chunked reads.
* Store sliding window in **Redis** with TTL.
* Ingest via **Kafka**, consume with async FastAPI workers.
* Persist correlated edges to **Parquet** for audit.
* Add **allow/deny** lists in `cfg/rules.yaml` for quick tuning.

---

## Deliverables you’ll have at the end

* `correlated.parquet` — joined CDR↔IPDR with VoIP flags + ASN/ISP
* `groups.jsonl` — time-windowed multiparty clusters
* (Optional) Running **WebSocket API** streaming these groups in real time

---

If you want, I can generate the **CLI scaffold (files + runnable code)** matching this plan so you just drop your CSVs and run it.
# VoIPTracer