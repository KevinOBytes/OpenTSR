# OpenTSR Capabilities & Features

**The "Flight Data Recorder" for the Agentic Age.**

OpenTSR is not just a logging format; it is a **Cyber-Physical Safety Protocol**. Below are the core capabilities that distinguish it from legacy schemas like OCSF or CEF.

## 1. Native Vector Support (The "AI-First" Feature)
Legacy logs are text. OpenTSR signals are **mathematical concepts**.
* **Feature:** `vector` field included in the core schema.
* **Benefit:** Allows immediate RAG (Retrieval-Augmented Generation). An AI agent can ask, *"Have we seen this chemical pressure spike before?"* and get an answer based on semantic similarity, not just keyword matching.

## 2. High-Assurance Veracity
In an age of hallucinations, you need to know what is real.
* **Feature:** Explicit `veracity_score` and `hazard_flag`.
* **Benefit:** Downstream control systems can automatically reject low-veracity signals.
    * *Example:* "If `veracity < 0.9`, do NOT open the pressure valve, even if the Agent requests it."

## 3. Physical Context Awareness
Cyber logs ignore the physical world. OpenTSR unites them.
* **Feature:** Specialized `physical:sensor` vocabulary.
* **Benefit:** Correlates bit-level events with atom-level consequences.
    * *Use Case:* Correlating a **Network Intrusion** (Cyber) with a **Temperature Spike** (Physical) in the same vector space to detect Stuxnet-style attacks.

## 4. Agentic Governance
Built for the Google SAIF and MITRE ATLAS era.
* **Feature:** `agent_id` and `action_intent` fields.
* **Benefit:** Provides a distinct audit trail for **Autonomous Agents**. separating "Human Actions" from "AI Actions" for liability and debugging.

## 5. Zero-ETL Ingestion
Stop writing parsers.
* **Feature:** Strict JSON-LD Schema.
* **Benefit:** Signals are "Analysis Ready" the moment they are generated. TAREOps (and other compliant engines) can index them instantly without complex transformation pipelines.

## 6. Hybrid Storage Architecture
* **Feature:** Split-Brain Data Handling.
* **Benefit:**
    * **Hot Path:** Vectors go to Vector DB (Cloudflare Vectorize) for instant recall.
    * **Cold Path:** Raw JSON goes to Object Storage (R2) for cheap, immutable compliance logging.

---
**Ready to implement?**
See [REQUIREMENTS.md](./REQUIREMENTS.md) for the technical constraints required to unlock these features.