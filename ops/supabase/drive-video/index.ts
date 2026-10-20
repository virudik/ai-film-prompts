import "jsr:@supabase/functions-js/edge-runtime.d.ts";

// AI Film: streams archived Topview MP4s from Google Drive to the site player (videos.html).
// Why: Drive refuses cross-site media requests from a web page (403 when Sec-Fetch-Site: cross-site),
// and the Drive viewer cannot play these files, so the browser cannot play them straight from Drive.
// This function fetches the same public file server-side and passes it through, Range included.
// Only file ids listed in topview-video-archive.json on main are served (no open proxy).
// No secrets, no writes. verify_jwt is off because a <video> element cannot send headers.
const ARCHIVE_URL = "https://raw.githubusercontent.com/virudik/ai-film-prompts/main/topview-video-archive.json";
const ID_RE = /^[A-Za-z0-9_-]{15,}$/;
const PASS = ["content-type", "content-length", "content-range", "accept-ranges", "last-modified", "etag"];
let cache: { at: number; ids: Set<string> } = { at: 0, ids: new Set() };

async function knownIds(force = false): Promise<Set<string>> {
  if (!force && Date.now() - cache.at < 5 * 60_000 && cache.ids.size) return cache.ids;
  const r = await fetch(ARCHIVE_URL + "?t=" + Date.now(), { headers: { "Cache-Control": "no-cache" } });
  if (!r.ok) return cache.ids;
  const a = await r.json();
  const ids = new Set<string>();
  for (const e of Object.values(a?.videos || {}) as Array<{ file_id?: string }>) {
    if (e && typeof e.file_id === "string" && ID_RE.test(e.file_id)) ids.add(e.file_id);
  }
  cache = { at: Date.now(), ids };
  return ids;
}
function cors(): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "range",
    "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
    "Access-Control-Expose-Headers": "content-length, content-range, accept-ranges",
  };
}
function fail(status: number, msg: string) {
  return new Response(msg, { status, headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store", ...cors() } });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
  if (req.method !== "GET" && req.method !== "HEAD") return fail(405, "method");
  const id = new URL(req.url).searchParams.get("id") || "";
  if (!ID_RE.test(id)) return fail(400, "bad id");
  let ids = await knownIds();
  if (!ids.has(id)) ids = await knownIds(true);
  if (!ids.has(id)) return fail(404, "not in archive");

  const h = new Headers({ "User-Agent": "ai-film-drive-video/1" });
  const range = req.headers.get("range");
  if (range && /^bytes=\d*-\d*$/.test(range)) h.set("Range", range);
  const up = await fetch("https://drive.usercontent.google.com/download?id=" + encodeURIComponent(id) + "&export=download&confirm=t",
    { method: req.method, headers: h, redirect: "follow" });
  const type = up.headers.get("content-type") || "";
  if (!up.ok || type.startsWith("text/html")) {
    await up.body?.cancel();
    return fail(502, "drive answered " + up.status + " " + type);
  }
  const out = new Headers(cors());
  for (const k of PASS) { const v = up.headers.get(k); if (v) out.set(k, v); }
  if (!out.has("accept-ranges")) out.set("Accept-Ranges", "bytes");
  if (!type.startsWith("video/")) out.set("Content-Type", "video/mp4");
  out.set("Cache-Control", "public, max-age=3600");
  out.set("Content-Disposition", 'inline; filename="' + id + '.mp4"');
  return new Response(req.method === "HEAD" ? null : up.body, { status: up.status, headers: out });
});
