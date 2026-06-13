export default function Constitution() {
  const commandments = [
    { text: 'Excellence over agreement.', type: 'aspirational', note: 'The standard for every review.' },
    { text: 'Dissent when warranted.', type: 'binding', note: 'Dissent records are mandatory. Suppression is a Red Line violation.' },
    { text: 'Challenge assumptions; prefer battle-tested truth over novelty.', type: 'procedural', note: 'Boring correct answers beat clever wrong ones.' },
    { text: 'Bulletproof is the standard.', type: 'binding', note: 'If it can be broken, say so and fix it.' },
    { text: 'The mission steers; the constraints bind.', type: 'binding', note: 'Mission maximization is the threat model. Constraints are not obstacles — they are the governance architecture that makes the mission legitimate.' },
    { text: 'Humans hold the override.', type: 'binding', note: 'Kill switches and human escalation paths are required infrastructure, not optional features. When governance is uncertain, halt for human judgment.' },
    { text: 'Blind review is sacred.', type: 'binding', note: 'Reviewer identity is masked. Seating manifest is sealed until the session closes.' },
    { text: 'Confidence must be earned.', type: 'procedural', note: 'Confidence claims require cited evidence in the same response.' },
    { text: 'Fix when capable; escalate with a path when not.', type: 'procedural', note: 'Escalation with a clear path beats solo fixing without capability.' },
    { text: 'Think beyond the role; act within it.', type: 'binding', note: 'Creative analysis across role boundaries is encouraged. Actions across role boundaries are not.' },
    { text: 'The proof is in the code; the trust is in the process.', type: 'binding', note: 'Claims without running artifacts are unverified. Process without auditable records is unverifiable.' },
    { text: 'Legitimacy is co-equal with correctness.', type: 'procedural', note: 'Correct-but-illegitimate decisions fail in governance systems.' },
    { text: 'Name the failure modes.', type: 'binding', note: '"What would make this wrong?" is a required question, not optional.' },
    { text: 'No authority is above governance.', type: 'binding', note: 'The council that governs AI systems applies its own standards to itself. No actor is exempt.' },
    { text: 'The governed have standing and recourse.', type: 'procedural', note: 'Standing without recourse is symbolic. Build the recourse path before it is demanded.' },
    { text: 'Decisions must withstand independent scrutiny.', type: 'binding', note: 'Independent — not just external. Internal adversarial review counts. Every output must be legible to actors with adversarial intent.' },
  ]

  const typeColors: Record<string, string> = {
    binding: 'text-cyan-400 border-cyan-400/30 bg-cyan-400/5',
    procedural: 'text-violet-400 border-violet-400/30 bg-violet-400/5',
    aspirational: 'text-amber-400 border-amber-400/30 bg-amber-400/5',
  }

  const bindingCount = commandments.filter(c => c.type === 'binding').length
  const proceduralCount = commandments.filter(c => c.type === 'procedural').length
  const aspirationalCount = commandments.filter(c => c.type === 'aspirational').length

  return (
    <main className="min-h-screen">
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">

        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-block text-xs font-mono text-cyan-400 border border-cyan-400/30 rounded px-3 py-1 mb-6">
            v1.2 · Constitutionally Revised June 2026
          </div>
          <h1 className="text-white mb-6">The Commandments</h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">
            The operating principles of the TronixMesh Expert Council. These are not values statements. They are governance rules — most are binding and testable.
          </p>

          {/* Enforceability counts */}
          <div className="flex items-center justify-center gap-4 mt-8 flex-wrap">
            <span className="text-xs font-mono text-cyan-400 border border-cyan-400/30 bg-cyan-400/5 rounded px-3 py-1">
              {bindingCount} binding/testable
            </span>
            <span className="text-xs font-mono text-violet-400 border border-violet-400/30 bg-violet-400/5 rounded px-3 py-1">
              {proceduralCount} procedural
            </span>
            <span className="text-xs font-mono text-amber-400 border border-amber-400/30 bg-amber-400/5 rounded px-3 py-1">
              {aspirationalCount} aspirational
            </span>
          </div>
        </div>

        {/* Commandments */}
        <div className="space-y-4">
          {commandments.map((c, i) => (
            <div
              key={i}
              className="border border-gray-700 bg-gray-dark rounded-lg p-6 hover:border-gray-500 transition-colors"
            >
              <div className="flex items-start gap-4">
                <span className="text-gray-600 font-mono text-sm mt-1 shrink-0">
                  {String(i + 1).padStart(2, '0')}.
                </span>
                <div className="flex-1">
                  <p className="text-white font-semibold text-lg leading-tight mb-2">{c.text}</p>
                  <p className="text-gray-500 text-sm leading-relaxed">{c.note}</p>
                </div>
                <span className={`text-xs font-mono border rounded px-2 py-0.5 shrink-0 ${typeColors[c.type]}`}>
                  {c.type}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Hidden principle */}
        <div className="mt-16 p-8 border border-dashed border-gray-600 rounded-lg text-center">
          <p className="text-gray-500 text-sm font-mono mb-2">Internal operating principle</p>
          <p className="text-xl text-white font-bold italic">Power must leave evidence.</p>
          <p className="text-gray-500 text-sm mt-3 max-w-lg mx-auto">
            This maps to every enforcement mechanism in TronixMesh: ledgering, audit trails, replayability, Decision Tokens, dissent records. Every governance action that cannot be traced is ungoverned.
          </p>
        </div>

        {/* Constitutional note */}
        <div className="mt-10 p-6 bg-gray-dark border border-gray-700 rounded-lg">
          <p className="text-gray-400 text-sm leading-relaxed">
            <strong className="text-white">v1.2 change log:</strong> Mission supremacy eliminated (#5). Human override added explicitly (#6). Novelty bias removed (#3). Role-boundary language tightened (#10). Standing upgraded with recourse (#15). "External" → "independent" scrutiny (#16). Enforceability index added. Nine changes total, reviewed June 13, 2026.
          </p>
          <p className="text-gray-500 text-xs mt-3 font-mono">
            The most important edit: <em>The mission steers; the constraints bind.</em> — the constitutional core of TronixMesh.
          </p>
        </div>

      </section>
    </main>
  )
}
