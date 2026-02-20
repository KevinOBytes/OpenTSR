import { randomBytes } from "node:crypto";
import { z } from "zod";

const UUID_V7_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const SHA256_REGEX = /^[A-Fa-f0-9]{64}$/;
const MAX_INT64 = 9_223_372_036_854_775_807;

export const OriginSchema = z
  .object({
    kind: z.enum(["llm_agent", "sensor", "service", "human_operator", "simulator"]),
    source_id: z.string().min(1),
    namespace: z.string().min(1).optional(),
    device_id: z.string().min(1).optional(),
    software_version: z.string().min(1).optional(),
    region: z.string().min(1).optional()
  })
  .strict();

export const ActionIntentSchema = z
  .object({
    action: z.string().min(1),
    target: z.string().min(1),
    reason: z.string().min(1).optional(),
    requested_by: z.string().min(1).optional()
  })
  .strict();

export const SafetySchema = z
  .object({
    veracity_score: z.number().min(0.0).max(1.0),
    hazard_flag: z.boolean(),
    digital_signature: z.string().min(1).optional(),
    signature_alg: z.string().min(1).optional()
  })
  .strict();

export const TSRSignalSchema = z
  .object({
    "@context": z.literal("https://opentsr.org/context/v1"),
    "@type": z.literal("OpenTSRSignal"),
    schema_version: z.literal("1.0.0-draft").default("1.0.0-draft"),
    tsr_id: z.string().regex(UUID_V7_REGEX),
    tsr_timestamp_ns: z.number().int().nonnegative().max(MAX_INT64),
    env: z.enum(["dev", "staging", "prod"]),
    origin: OriginSchema,
    agent_id: z.string().min(1).optional(),
    action_intent: ActionIntentSchema.optional(),
    payload: z
      .record(z.unknown())
      .superRefine((payload, ctx) => {
        const blobUrl = payload["blob_url"];
        const sha256Hash = payload["sha256_hash"];
        if (blobUrl !== undefined && typeof sha256Hash !== "string") {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: "payload.sha256_hash is required when payload.blob_url is set"
          });
        }
        if (typeof sha256Hash === "string" && !SHA256_REGEX.test(sha256Hash)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: "payload.sha256_hash must be a 64-character hex digest"
          });
        }
      }),
    vector: z
      .array(z.number().min(-1.0).max(1.0))
      .superRefine((vector, ctx) => {
        if (vector.length !== 1024 && vector.length !== 1536) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: "vector length must be exactly 1024 or 1536"
          });
        }
      })
      .optional(),
    safety: SafetySchema,
    tags: z.array(z.string().min(1)).max(64).optional(),
    trace: z
      .object({
        trace_id: z.string().min(1).optional(),
        span_id: z.string().min(1).optional(),
        parent_span_id: z.string().min(1).optional()
      })
      .strict()
      .optional()
  })
  .strict()
  .superRefine((signal, ctx) => {
    if (signal.origin.kind === "llm_agent" && !signal.agent_id) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "agent_id is required when origin.kind is llm_agent"
      });
    }
    if (signal.origin.kind === "llm_agent" && !signal.action_intent) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "action_intent is required when origin.kind is llm_agent"
      });
    }
    if (signal.env === "prod" && !signal.safety.digital_signature) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "safety.digital_signature is required when env is prod"
      });
    }
    if (signal.safety.digital_signature && !signal.safety.signature_alg) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "safety.signature_alg is required when safety.digital_signature is present"
      });
    }
    if (signal.safety.signature_alg && !signal.safety.digital_signature) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "safety.digital_signature is required when safety.signature_alg is present"
      });
    }
  });

export type TSRSignal = z.infer<typeof TSRSignalSchema>;

function formatUuid(bytes: Uint8Array): string {
  const hex = [...bytes].map((value) => value.toString(16).padStart(2, "0"));
  return `${hex.slice(0, 4).join("")}-${hex.slice(4, 6).join("")}-${hex.slice(6, 8).join("")}-${hex.slice(8, 10).join("")}-${hex.slice(10, 16).join("")}`;
}

export function generateUuidV7(): string {
  const timestampMs = BigInt(Date.now());
  if (timestampMs < 0n) {
    throw new Error("Invalid system time while generating UUIDv7");
  }
  if (timestampMs >= (1n << 48n)) {
    throw new Error("timestamp milliseconds exceed UUIDv7 range");
  }

  const random = randomBytes(10);
  const bytes = new Uint8Array(16);

  bytes[0] = Number((timestampMs >> 40n) & 0xffn);
  bytes[1] = Number((timestampMs >> 32n) & 0xffn);
  bytes[2] = Number((timestampMs >> 24n) & 0xffn);
  bytes[3] = Number((timestampMs >> 16n) & 0xffn);
  bytes[4] = Number((timestampMs >> 8n) & 0xffn);
  bytes[5] = Number(timestampMs & 0xffn);
  bytes[6] = 0x70 | (random[0]! & 0x0f);
  bytes[7] = random[1]!;
  bytes[8] = 0x80 | (random[2]! & 0x3f);
  bytes[9] = random[3]!;
  bytes[10] = random[4]!;
  bytes[11] = random[5]!;
  bytes[12] = random[6]!;
  bytes[13] = random[7]!;
  bytes[14] = random[8]!;
  bytes[15] = random[9]!;

  return formatUuid(bytes);
}

export function nowTimestampNs(): number {
  const timestampNs = Math.trunc(Date.now() * 1_000_000);
  if (timestampNs < 0 || timestampNs > MAX_INT64) {
    throw new Error("timestamp_ns is out of int64 bounds");
  }
  return timestampNs;
}

type CreateSignalInput = Omit<TSRSignal, "@context" | "@type" | "tsr_id" | "tsr_timestamp_ns" | "schema_version"> &
  Partial<Pick<TSRSignal, "tsr_id" | "tsr_timestamp_ns" | "schema_version">>;

export function createSignal(input: CreateSignalInput): TSRSignal {
  const merged: Record<string, unknown> = {
    "@context": "https://opentsr.org/context/v1",
    "@type": "OpenTSRSignal",
    schema_version: input.schema_version ?? "1.0.0-draft",
    tsr_id: input.tsr_id ?? generateUuidV7(),
    tsr_timestamp_ns: input.tsr_timestamp_ns ?? nowTimestampNs(),
    env: input.env,
    origin: input.origin,
    payload: input.payload,
    safety: input.safety
  };
  if (input.agent_id !== undefined) {
    merged["agent_id"] = input.agent_id;
  }
  if (input.action_intent !== undefined) {
    merged["action_intent"] = input.action_intent;
  }
  if (input.vector !== undefined) {
    merged["vector"] = input.vector;
  }
  if (input.tags !== undefined) {
    merged["tags"] = input.tags;
  }
  if (input.trace !== undefined) {
    merged["trace"] = input.trace;
  }
  return TSRSignalSchema.parse(merged);
}

export function validateSignal(input: unknown): TSRSignal {
  return TSRSignalSchema.parse(input);
}
