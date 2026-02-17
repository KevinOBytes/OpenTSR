# INFRASTRUCTURE.md - Cloud & Resource State

## Philosophy
**"Cloudflare First, NVIDIA Accelerated."**
We use Cloudflare for the "Edge" (Speed/Ingest) and NVIDIA for the "Brain" (Training/Embeddings).

## 1. The Bedrock (Managed via Terraform)
*Location: `infra/main.tf`*
* **DNS:** `tareops.com`, `opentsr.org` (Future).
* **Object Storage (R2):**
    * `bucket: tare-signals-prod` (Retention: 1 year).
    * `bucket: tare-signals-dev` (Retention: 7 days).
* **Access:** Cloudflare Zero Trust policies for developer access.

## 2. The Application (Managed via Wrangler)
*Location: `wrangler.toml`*
* **Workers:**
    * `ingest-worker`: Public API endpoint.
    * `sentinel-worker`: Async processor for safety checks.
* **Vectorize:**
    * `index: tare-vectors-v1` (Dimensions: 1536, Metric: Cosine).
* **AI Gateway:**
    * `gateway: tare-ai` (Rate limiting & caching for OpenAI/NVIDIA calls).

## 3. External Dependencies
* **NVIDIA Inception:**
    * Deep Learning Institute (DLI) Credits.
    * DGX Cloud (for retraining the Sentinel model).
* **Neon:** Serverless Postgres (Metadata).