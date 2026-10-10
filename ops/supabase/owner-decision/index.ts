import "jsr:@supabase/functions-js/edge-runtime.d.ts";

// AI Film owner-only decisions and free-text owner tasks (v6, 10.10.2026: + in_film).
// Custom auth: header x-owner-key must equal the OWNER_DECISION_KEY secret (the owner's own
// password, set by the owner in the Supabase dashboard; never in HTML, GitHub or chat).
// verify_jwt is off on purpose because this check replaces it.
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const OWNER_KEY = Deno.env.get("OWNER_DECISION_KEY") || "";
const ALLOWED_ORIGINS = new Set(["https://virudik.github.io", "https://рудик.рф", "https://xn--d1aigvp.xn--p1ai"]);
const ACTIONS = new Set(["accept", "redo", "to_montage", "scene_not_needed", "tv_drop_task", "tv_mark_status", "owner_task", "in_film"]);
const TV_STATUSES = new Set(["result_ok", "result_bad", "not_waiting", "failed"]);

function cors(origin: string | null) {
  const allowed = origin && ALLOWED_ORIGINS.has(origin) ? origin : "https://virudik.github.io";
  return { "Access-Control-Allow-Origin": allowed, "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-owner-key", "Access-Control-Allow-Methods": "POST, OPTIONS", "Vary": "Origin" };
}
function json(body: unknown, status: number, origin: string | null) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...cors(origin) } });
}
async function sha256(v: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(v));
  return Array.from(new Uint8Array(d)).map(b => b.toString(16).padStart(2, "0")).join("");
}
async function sameSecret(a: string, b: string) {
  const [x, y] = await Promise.all([sha256(a), sha256(b)]);
  let diff = 0; for (let i = 0; i < x.length; i++) diff |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return diff === 0;
}
async function db(path: string, init: RequestInit = {}) {
  const h = new Headers(init.headers || {});
  h.set("apikey", SERVICE_ROLE); h.set("Authorization", `Bearer ${SERVICE_ROLE}`); h.set("Content-Type", "application/json");
  return fetch(`${SUPABASE_URL}/rest/v1/${path}`, { ...init, headers: h });
}
async function failures(filter: string) {
  const since = new Date(Date.now() - 60 * 60 * 1000).toISOString();
  const r = await db(`owner_auth_failures?created_at=gte.${encodeURIComponent(since)}${filter}&select=id`);
  if (!r.ok) return 999;
  const rows = await r.json();
  return Array.isArray(rows) ? rows.length : 999;
}

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);
  if (origin && !ALLOWED_ORIGINS.has(origin)) return json({ error: "origin_not_allowed" }, 403, origin);
  if (OWNER_KEY.length < 6) return json({ error: "not_configured" }, 503, origin);

  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "unknown";
  const ipHash = await sha256(ip);
  if (await failures(`&ip_hash=eq.${ipHash}`) >= 5 || await failures("") >= 30) return json({ error: "locked_try_later" }, 429, origin);

  const key = req.headers.get("x-owner-key") || "";
  if (!(await sameSecret(key, OWNER_KEY))) {
    await db("owner_auth_failures", { method: "POST", headers: { Prefer: "return=minimal" }, body: JSON.stringify({ ip_hash: ipHash }) });
    return json({ error: "forbidden" }, 403, origin);
  }

  let p: any; try { p = await req.json(); } catch { return json({ error: "invalid_json" }, 400, origin); }
  const op = String(p?.op ?? "decide");
  if (op === "verify") return json({ ok: true }, 200, origin);
  if (op === "list") {
    const r = await db("owner_decisions?select=id,created_at,scene_id,action,task_id,value,note,status,applied_at,result_note&order=created_at.desc&limit=50");
    return r.ok ? json({ ok: true, decisions: await r.json() }, 200, origin) : json({ error: "list_failed" }, 500, origin);
  }
  if (op === "cancel") {
    const id = String(p?.id ?? "");
    if (!/^[0-9a-f-]{36}$/i.test(id)) return json({ error: "invalid_id" }, 400, origin);
    const r = await db(`owner_decisions?id=eq.${id}&status=in.(pending,needs_owner)`, { method: "PATCH", headers: { Prefer: "return=representation" }, body: JSON.stringify({ status: "superseded", result_note: "cancelled by owner" }) });
    return r.ok ? json({ ok: true, changed: (await r.json()).length }, 200, origin) : json({ error: "cancel_failed" }, 500, origin);
  }
  if (op !== "decide") return json({ error: "invalid_op" }, 400, origin);

  const action = String(p?.action ?? "");
  const hasScene = p?.scene_id !== undefined && p?.scene_id !== null && p?.scene_id !== "";
  const scene = hasScene ? Number(p.scene_id) : null;
  const task = p?.task_id ? String(p.task_id).toLowerCase() : null;
  const value = p?.value ? String(p.value) : null;
  const note = p?.note ? String(p.note).trim().slice(0, 2000) : null;
  if (!ACTIONS.has(action)) return json({ error: "invalid_action" }, 400, origin);
  if (scene !== null && (!Number.isInteger(scene) || scene < 1 || scene > 999)) return json({ error: "invalid_scene" }, 400, origin);
  if (action !== "owner_task" && scene === null) return json({ error: "invalid_scene" }, 400, origin);
  if (action === "owner_task" && (!note || note.length < 3)) return json({ error: "note_required" }, 400, origin);
  if (action !== "owner_task" && note && note.length > 500) return json({ error: "note_too_long" }, 400, origin);
  if (task && !/^[0-9a-f]{32}$/.test(task)) return json({ error: "invalid_task" }, 400, origin);
  if (action.startsWith("tv_") && !task) return json({ error: "task_required" }, 400, origin);
  if (action === "tv_mark_status" && !(value && TV_STATUSES.has(value))) return json({ error: "invalid_status" }, 400, origin);

  const r = await db("owner_decisions?select=id,created_at,scene_id,action,task_id,value,status", { method: "POST", headers: { Prefer: "return=representation" }, body: JSON.stringify({ scene_id: scene, action, task_id: task, value, note }) });
  if (!r.ok) { console.error("insert failed", await r.text()); return json({ error: "insert_failed" }, 500, origin); }
  const rows = await r.json();
  return json({ ok: true, decision: rows?.[0] ?? null }, 201, origin);
});
