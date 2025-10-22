import { PrismaClient } from "../src/generated/prisma";

const prisma = new PrismaClient();

const cards = [
  // BODY CARDS
  {
    type: "body",
    state: "tension",
    title: "Body Tension",
    guidingPrompt:
      "Notice where you're holding tension and what might be creating this pattern.",
    questions: [
      {
        prompt: "Where in your body?",
        inputType: "text",
      },
      {
        prompt: "What's causing this?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user is experiencing body tension. Provide a brief Socratic reflection (2-3 sentences) asking what the tension might be protecting or teaching them. Reference their specific location and cause. Be warm and non-judgmental.",
    icon: "🫀",
    color: "#EF4444",
    deck: "core",
    order: 1,
    ascendingStates: ["awareness", "ease"],
    descendingStates: ["depletion"],
    breaksPatternOf: [],
  },
  {
    type: "body",
    state: "awareness",
    title: "Body Awareness",
    guidingPrompt:
      "What is your body telling you in this moment? Listen to what sensation is strongest.",
    questions: [
      {
        prompt: "What sensation is strongest?",
        inputType: "text",
      },
      {
        prompt: "What is it asking for?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user is experiencing body awareness - a breakthrough state. Acknowledge their presence with their body. Ask one question that deepens the awareness or points to action. 2-3 sentences.",
    icon: "🫀",
    color: "#EF4444",
    deck: "core",
    order: 2,
    ascendingStates: ["ease", "restoration"],
    descendingStates: [],
    breaksPatternOf: ["tension", "depletion"],
  },
  {
    type: "body",
    state: "ease",
    title: "Body Ease",
    guidingPrompt:
      "Notice how this ease feels different. What allowed this softening to happen?",
    questions: [
      {
        prompt: "How does ease feel?",
        inputType: "text",
      },
      {
        prompt: "What created this shift?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user is experiencing body ease. Reflect on what created this state and how they might recognize or recreate it. 2-3 sentences. Warm and encouraging.",
    icon: "🫀",
    color: "#EF4444",
    deck: "core",
    order: 3,
    ascendingStates: ["flow", "restoration"],
    descendingStates: [],
    breaksPatternOf: [],
  },
  {
    type: "body",
    state: "depletion",
    title: "Body Depletion",
    guidingPrompt:
      "Notice how depleted your body feels and what's been asked of it.",
    questions: [
      {
        prompt: "How depleted? (1-10)",
        inputType: "text",
      },
      {
        prompt: "What's been demanded of it?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's body is depleted. Acknowledge the depletion without judgment. Ask what kind of rest or restoration their body is asking for. 2-3 sentences.",
    icon: "🫀",
    color: "#EF4444",
    deck: "core",
    order: 4,
    ascendingStates: ["rest", "awareness"],
    descendingStates: ["exhaustion"],
    breaksPatternOf: [],
  },
  {
    type: "body",
    state: "rest",
    title: "Body Rest",
    guidingPrompt:
      "What kind of rest is your body asking for? What can you give it right now?",
    questions: [
      {
        prompt: "What type of rest?",
        inputType: "text",
      },
      {
        prompt: "What's one thing you can do?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user recognizes their need for rest. Acknowledge this awareness. Encourage even the smallest action toward restoration. 2-3 sentences.",
    icon: "🫀",
    color: "#EF4444",
    deck: "core",
    order: 5,
    ascendingStates: ["restoration", "ease"],
    descendingStates: [],
    breaksPatternOf: ["depletion"],
  },

  // ENERGY CARDS
  {
    type: "energy",
    state: "depletion",
    title: "Energy Depletion",
    guidingPrompt:
      "Notice what drained your energy and how empty you feel right now.",
    questions: [
      {
        prompt: "What drained you?",
        inputType: "text",
      },
      {
        prompt: "How empty? (1-10)",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's energy is depleted. Acknowledge what drained them. Ask what their energy needs to restore - not what they should do, but what energy itself is asking for. 2-3 sentences.",
    icon: "⚡",
    color: "#F59E0B",
    deck: "core",
    order: 6,
    ascendingStates: ["recovery", "restoration"],
    descendingStates: ["collapse"],
    breaksPatternOf: [],
  },
  {
    type: "energy",
    state: "flow",
    title: "Energy Flow",
    guidingPrompt:
      "Notice the quality of your energy right now and when you last felt it shift.",
    questions: [
      {
        prompt: "What's the quality?",
        inputType: "text",
      },
      {
        prompt: "When did it shift?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's energy is flowing. Reflect on what created or allowed this flow. Ask what they notice about the conditions that support it. 2-3 sentences.",
    icon: "⚡",
    color: "#F59E0B",
    deck: "core",
    order: 7,
    ascendingStates: ["vitality", "clarity"],
    descendingStates: [],
    breaksPatternOf: ["stuck"],
  },
  {
    type: "energy",
    state: "restoration",
    title: "Energy Restoration",
    guidingPrompt:
      "Notice what restored your energy and whether you can do more of it.",
    questions: [
      {
        prompt: "What restored you?",
        inputType: "text",
      },
      {
        prompt: "Can you do more of that?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's energy is being restored. Celebrate what worked. Ask how they might remember this when energy depletes again. 2-3 sentences.",
    icon: "⚡",
    color: "#F59E0B",
    deck: "core",
    order: 8,
    ascendingStates: ["joy", "gratitude", "flow"],
    descendingStates: [],
    breaksPatternOf: ["depletion"],
  },
  {
    type: "energy",
    state: "stuck",
    title: "Energy Stuck",
    guidingPrompt:
      "Notice where your energy is stuck and what wants to move but can't.",
    questions: [
      {
        prompt: "Where is it stuck?",
        inputType: "text",
      },
      {
        prompt: "What wants to move?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's energy is stuck. Ask what might be holding it in place - not to fix, but to bring awareness. What would movement look like? 2-3 sentences.",
    icon: "⚡",
    color: "#F59E0B",
    deck: "core",
    order: 9,
    ascendingStates: ["awareness", "flow"],
    descendingStates: ["depletion"],
    breaksPatternOf: [],
  },
  {
    type: "energy",
    state: "activation",
    title: "Energy Activation",
    guidingPrompt:
      "Is this activation anxiety or aliveness? Notice where you feel it in your body.",
    questions: [
      {
        prompt: "Anxiety or aliveness?",
        inputType: "text",
      },
      {
        prompt: "Where do you feel it?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's energy is activated. Help them discern between anxiety (contractive) and aliveness (expansive). Ask what their body knows about this activation. 2-3 sentences.",
    icon: "⚡",
    color: "#F59E0B",
    deck: "core",
    order: 10,
    ascendingStates: ["engaged", "flow"],
    descendingStates: ["anxious", "tension"],
    breaksPatternOf: [],
  },

  // MIND CARDS
  {
    type: "mind",
    state: "fog",
    title: "Mind Fog",
    guidingPrompt:
      "Notice what's making your mind foggy and what needs clearing.",
    questions: [
      {
        prompt: "What's creating fog?",
        inputType: "text",
      },
      {
        prompt: "What needs clearing?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's mind is foggy. Ask what the fog might be protecting them from seeing, or what clarity might require. 2-3 sentences. Non-judgmental.",
    icon: "🧠",
    color: "#3B82F6",
    deck: "core",
    order: 11,
    ascendingStates: ["clarity", "awareness"],
    descendingStates: ["confusion"],
    breaksPatternOf: [],
  },
  {
    type: "mind",
    state: "clarity",
    title: "Mind Clarity",
    guidingPrompt:
      "Notice what created this clarity and what you can see now that was hidden.",
    questions: [
      {
        prompt: "What created clarity?",
        inputType: "text",
      },
      {
        prompt: "What can you see now?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user has mental clarity. Acknowledge what they can now see. Ask what this clarity wants them to do or know. 2-3 sentences.",
    icon: "🧠",
    color: "#3B82F6",
    deck: "core",
    order: 12,
    ascendingStates: ["insight", "integration"],
    descendingStates: [],
    breaksPatternOf: ["fog", "confusion"],
  },
  {
    type: "mind",
    state: "worry",
    title: "Mind Worry",
    guidingPrompt:
      "Notice what worry is loudest right now and what's beneath it.",
    questions: [
      {
        prompt: "What's the worry?",
        inputType: "text",
      },
      {
        prompt: "What's beneath it?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user is worrying. Ask what the worry is trying to protect or prepare them for. Help them see the worry's positive intention without judgment. 2-3 sentences.",
    icon: "🧠",
    color: "#3B82F6",
    deck: "core",
    order: 13,
    ascendingStates: ["awareness", "clarity"],
    descendingStates: ["anxiety", "racing"],
    breaksPatternOf: [],
  },
  {
    type: "mind",
    state: "racing",
    title: "Mind Racing",
    guidingPrompt:
      "Notice what your mind is racing toward or away from, and what happens if you pause.",
    questions: [
      {
        prompt: "Racing toward or away from what?",
        inputType: "text",
      },
      {
        prompt: "What if you pause?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user's mind is racing. Ask what it's running from or toward. What would it mean to pause? 2-3 sentences. Warm, spacious.",
    icon: "🧠",
    color: "#3B82F6",
    deck: "core",
    order: 14,
    ascendingStates: ["focus", "clarity"],
    descendingStates: ["overwhelm", "anxiety"],
    breaksPatternOf: [],
  },
  {
    type: "mind",
    state: "present",
    title: "Mind Present",
    guidingPrompt:
      "Notice how aware you are in this moment and what brought you here.",
    questions: [
      {
        prompt: "How present are you?",
        inputType: "text",
      },
      {
        prompt: "What brought you here?",
        inputType: "text",
      },
    ],
    reflectionPrompt:
      "The user is present - a breakthrough state. Acknowledge this awareness. Ask what they notice from this place of presence. 2-3 sentences. Celebratory but grounded.",
    icon: "🧠",
    color: "#3B82F6",
    deck: "core",
    order: 15,
    ascendingStates: ["integration", "clarity", "flow"],
    descendingStates: [],
    breaksPatternOf: ["worry", "racing", "fog"],
  },
];

async function main() {
  console.log("🌱 Seeding cards...");

  // Clear existing cards
  await prisma.card.deleteMany({});
  console.log("🗑️  Cleared existing cards");

  // Create cards
  for (const card of cards) {
    await prisma.card.create({
      data: card,
    });
  }

  console.log(`✅ Created ${cards.length} cards`);
  console.log("🎉 Seeding complete!");
}

main()
  .catch((e) => {
    console.error("❌ Error seeding:", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
