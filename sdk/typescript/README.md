# OpenTSR TypeScript SDK

Reference TypeScript translator SDK for generating and validating OpenTSR JSON-LD payloads with Zod.

## Install

```bash
npm install
```

## Typecheck

```bash
npm run typecheck
```

## Example

```typescript
import { createSignal, validateSignal } from "@opentsr/sdk";

const signal = createSignal({
  env: "dev",
  origin: {
    kind: "llm_agent",
    source_id: "agent-core",
    namespace: "demo"
  },
  agent_id: "agent://agent-core",
  action_intent: {
    action: "evaluate",
    target: "task://42"
  },
  payload: {
    event: "evaluation_complete"
  },
  safety: {
    veracity_score: 0.8,
    hazard_flag: false
  }
});

validateSignal(signal);
```
