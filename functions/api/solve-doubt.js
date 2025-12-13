export async function onRequestPost({ request }) {
  let data = {};
  try {
    data = await request.json();
  } catch (_) {
    data = {};
  }
  const doubt = String(data?.doubt ?? data?.question ?? "");
  if (!doubt) {
    return new Response(
      JSON.stringify({ error: "Missing 'doubt' field" }),
      { status: 400, headers: { "content-type": "application/json" } }
    );
  }
  const message =
    `Here is an explanation for '${doubt}': ` +
    `[AI generated content would appear here in online mode; ` +
    `this is the offline mock running on Cloudflare Pages Functions]`;
  return new Response(JSON.stringify({ answer: message }), {
    headers: { "content-type": "application/json" }
  });
}
