export async function onRequestPost({ request }) {
  let data = {};
  try {
    data = await request.json();
  } catch (_) {
    data = {};
  }
  const topicRaw = data?.topic ?? "General";
  const topic = String(topicRaw);
  const rawPs = data?.problemsSolved ?? data?.problems_solved ?? 0;
  let problemsSolved = 0;
  try {
    problemsSolved = parseInt(rawPs ?? 0, 10);
  } catch (_) {
    problemsSolved = 0;
  }
  if (Number.isNaN(problemsSolved)) problemsSolved = 0;
  if (problemsSolved >= 5) {
    return new Response(
      JSON.stringify({
        status: "complete",
        message: "Quiz Complete! You have finished 5 questions."
      }),
      { headers: { "content-type": "application/json" } }
    );
  }
  const t = topic.toLowerCase();
  let payload;
  if (t.includes("matter")) {
    payload = {
      question:
        "Which of the following serves as evidence that matter is made of particles? (Offline Mode)",
      options: [
        "The smell of perfume spreads across a room",
        "Wood is hard",
        "Ice melts",
        "Iron rusts"
      ],
      answer: "The smell of perfume spreads across a room",
      hint: "Think about diffusion.",
      explanation:
        "Diffusion of gas particles shows that matter is particulate and particles are in motion."
    };
  } else if (t.includes("cell")) {
    payload = {
      question:
        "Which organelle is known as the powerhouse of the cell? (Offline Mode)",
      options: ["Nucleus", "Mitochondria", "Ribosome", "Golgi Apparatus"],
      answer: "Mitochondria",
      hint: "It generates ATP.",
      explanation: "Mitochondria release energy in the form of ATP."
    };
  } else {
    const templates = [
      {
        q: `Which of the following is true about ${topic}?`,
        options: [
          "It is related to physics",
          "It is related to music",
          "It involves cooking",
          "None of the above"
        ],
        a: "It is related to physics",
        why: "Because we are studying science!"
      },
      {
        q: `What is the primary characteristic of ${topic}?`,
        options: ["Constant change", "Stability", "Randomness", "Color"],
        a: "Constant change",
        why: "Most scientific phenomena involve change."
      }
    ];
    const pick = templates[Math.floor(Math.random() * templates.length)];
    payload = {
      question: `${pick.q} (Offline Mode)`,
      options: pick.options,
      answer: pick.a,
      hint: "Think logically.",
      explanation: pick.why
    };
  }
  return new Response(JSON.stringify(payload), {
    headers: { "content-type": "application/json" }
  });
}
