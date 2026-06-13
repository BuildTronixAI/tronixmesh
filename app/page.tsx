import Link from 'next/link'

export default function Home() {

  const comparisonRows = [
    { traditional: 'Trusts model behavior', tronix: 'Trusts governance, not the model' },
    { traditional: 'Safety is inside the model', tronix: 'Safety is outside and independent' },
    { traditional: 'Cannot independently halt', tronix: 'Cryptographically enforced halt' },
    { traditional: 'Difficult or impossible to audit', tronix: 'Cryptographic proof of every action' },
    { traditional: 'Stops working when model fails', tronix: 'Model-independent — survives any model' },
    { traditional: 'No recovery path', tronix: 'Degraded Execution Plane + re-entry gate' },
  ]

  const failureScenarios = [
    {
      icon: '🚫',
      title: 'Rogue Agent',
      scenario: 'Agent attempts an action outside its authorized scope.',
      result: 'Governance veto. Action blocked before execution. Event logged.',
      color: 'border-red-900/40',
    },
    {
      icon: '⚡',
      title: 'Quorum Collapse',
      scenario: 'A required signer goes offline or is compromised.',
      result: 'Automatic halt. No execution without quorum. System awaits recovery.',
      color: 'border-amber-900/40',
    },
    {
      icon: '🕐',
      title: 'Clock Corruption',
      scenario: 'Time source drifts or is manipulated by an attacker.',
      result: 'Execution suspended. Clock trust violated. Halt trigger fires.',
      color: 'border-orange-900/40',
    },
    {
      icon: '🔏',
      title: 'Audit Tampering',
      scenario: 'An actor attempts to alter a past record in the ledger.',
      result: 'Hash chain invalidates. Proof verification fails. Tamper is provable.',
      color: 'border-violet-900/40',
    },
    {
      icon: '💀',
      title: 'Governance Plane Failure',
      scenario: 'Primary governance layer becomes unavailable or compromised.',
      result: 'Authority migrates to isolated Degraded Execution Plane. Constitutional legitimacy preserved.',
      color: 'border-cyan-900/40',
    },
  ]

  const certTiers = [
    { name: 'Bronze', tag: 'TM-CERT-BRONZE', desc: 'Basic governance. Identity, authorization, audit trail.', color: 'text-amber-700' },
    { name: 'Silver', tag: 'TM-CERT-SILVER', desc: 'DEP-enabled. Fault isolation and recovery mechanisms.', color: 'text-gray-400' },
    { name: 'Gold', tag: 'TM-CERT-GOLD', desc: 'Full constitutional compliance. All 9 doctrines. 412 conformance tests.', color: 'text-yellow-400' },
    { name: 'Platinum', tag: 'TM-CERT-PLATINUM', desc: 'External audit certified. Independent third-party verification.', color: 'text-cyan-300' },
  ]

  return (
    <main className="min-h-screen">

      {/* ── HERO ──────────────────────────────────────────────────────── */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-36 text-center">
        <div className="inline-block text-xs font-mono text-blue border border-blue/30 rounded px-3 py-1 mb-8">
          Runtime Governance Substrate · Patent Pending
        </div>
        <h1 className="text-white mb-8 leading-tight">
          AI systems can fail, drift, collude,<br className="hidden md:block" />
          or hallucinate authority.<br className="hidden md:block" />
          <span className="text-blue">TronixMesh governs the ones that can't be wrong.</span>
        </h1>
        <p className="text-xl text-gray-400 mb-4 max-w-3xl mx-auto leading-relaxed">
          TronixMesh is the governance layer that can halt, constrain, recover, and prove what happened — even when the AI itself is wrong.
        </p>
        <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-12 leading-relaxed">
          The Control Plane is <strong className="text-white">model-independent.</strong> Its authority derives from a cryptographically committed constitutional ruleset — not from any AI model's capability, training, or output. It may refuse execution even when all agents agree.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/contact" className="px-8 py-4 bg-blue text-white font-semibold rounded hover:bg-opacity-80 transition text-lg">
            Start a Conversation
          </Link>
          <Link href="/architecture" className="px-8 py-4 border border-gray-600 text-gray-light font-semibold rounded hover:border-blue hover:text-blue transition text-lg">
            View Architecture
          </Link>
        </div>
      </section>

      {/* ── THE REAL QUESTION ────────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-20">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
          <p className="text-gray-400 text-xl leading-relaxed mb-6">
            Autonomous systems will eventually control money, infrastructure, logistics, healthcare, and defense.
          </p>
          <p className="text-gray-400 text-xl leading-relaxed mb-10">
            The question is no longer whether AI can act.<br />
            <strong className="text-white">The question is who governs the AI.</strong>
          </p>
          <p className="text-gray-300 text-lg leading-relaxed max-w-2xl mx-auto">
            TronixMesh is a constitutional governance substrate that provides cryptographic authority, independent oversight, fault isolation, recovery mechanisms, and provable accountability for autonomous systems.
          </p>
        </div>
      </section>

      {/* ── ARCHITECTURE DIAGRAM ────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-20 bg-gray-dark/30">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-white mb-4">How It Works</h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Every agent action flows through the governance layer. No exceptions.
            </p>
          </div>

          {/* Normal flow */}
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <p className="text-xs font-mono text-blue mb-6 uppercase tracking-widest">Normal Execution Flow</p>
              <div className="space-y-2">
                {[
                  { label: 'AI Agents', note: 'Request execution authority' },
                  { label: 'TronixMesh Governance Layer', note: 'Evaluates against constitutional ruleset', highlight: true },
                  { label: 'Control Plane', note: 'Issues execution token (lease-based)' },
                  { label: 'Execution Authority', note: 'Cryptographically authorized action' },
                  { label: 'Audit Ledger', note: 'Hash-chained, append-only, signed' },
                ].map((step, i, arr) => (
                  <div key={i}>
                    <div className={`px-5 py-3 rounded-lg border text-sm font-medium ${
                      step.highlight
                        ? 'border-blue bg-blue/10 text-blue'
                        : 'border-gray-700 bg-gray-dark text-gray-300'
                    }`}>
                      <span className="font-bold">{step.label}</span>
                      <span className="text-gray-500 font-normal ml-2 text-xs">{step.note}</span>
                    </div>
                    {i < arr.length - 1 && (
                      <div className="text-center text-gray-600 py-1 text-lg">↓</div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Fault flow */}
            <div>
              <p className="text-xs font-mono text-red-400 mb-6 uppercase tracking-widest">Fault & Recovery Flow</p>
              <div className="space-y-2">
                {[
                  { label: 'Fault Detected', note: '7 enumerated halt triggers', color: 'border-red-800/60 bg-red-900/10 text-red-300' },
                  { label: 'HALT', note: 'Execution suspended immediately', color: 'border-red-600 bg-red-900/20 text-red-400 font-black' },
                  { label: 'Degraded Execution Plane', note: 'Isolated authority migration', color: 'border-amber-700/60 bg-amber-900/10 text-amber-300', highlight: true },
                  { label: 'Recovery Proof Package', note: 'Dual-admin attestation required', color: 'border-yellow-700/60 bg-yellow-900/10 text-yellow-300' },
                  { label: 'Re-entry Gate', note: 'Constitutional legitimacy re-established', color: 'border-cyan-700/60 bg-cyan-900/10 text-cyan-300' },
                ].map((step, i, arr) => (
                  <div key={i}>
                    <div className={`px-5 py-3 rounded-lg border text-sm font-medium ${step.color}`}>
                      <span className="font-bold">{step.label}</span>
                      <span className="opacity-70 font-normal ml-2 text-xs">{step.note}</span>
                    </div>
                    {i < arr.length - 1 && (
                      <div className="text-center text-gray-600 py-1 text-lg">↓</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* DEP callout */}
          <div className="mt-14 p-8 border border-cyan-800/40 bg-cyan-900/5 rounded-lg">
            <p className="text-xs font-mono text-cyan-400 mb-3 uppercase tracking-widest">Degraded Execution Plane — Key Innovation</p>
            <p className="text-white text-lg font-semibold mb-2">
              If the primary governance plane becomes compromised, TronixMesh migrates authority into an isolated Degraded Execution Plane while preserving constitutional legitimacy.
            </p>
            <p className="text-gray-400 text-sm">
              Q<sub>DEP</sub> ≥ Q<sub>MAIN</sub> + ⌈M/4⌉ — higher quorum required in degraded state. The system becomes harder to authorize as it becomes more compromised. Patent pending.
            </p>
          </div>
        </div>
      </section>

      {/* ── WHY EXISTING SAFETY FAILS ───────────────────────────────── */}
      <section className="border-t border-gray-700 py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-white mb-4">Why Existing AI Safety Isn't Enough</h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Model-level safety fails when the model is wrong. TronixMesh operates outside the model.
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="text-left py-3 px-4 text-gray-500 font-mono text-xs uppercase tracking-wide">Traditional AI Safety</th>
                  <th className="text-left py-3 px-4 text-blue font-mono text-xs uppercase tracking-wide">TronixMesh</th>
                </tr>
              </thead>
              <tbody>
                {comparisonRows.map((row, i) => (
                  <tr key={i} className="border-b border-gray-800 hover:bg-gray-dark/40 transition-colors">
                    <td className="py-4 px-4 text-gray-500">{row.traditional}</td>
                    <td className="py-4 px-4 text-gray-200 font-medium">{row.tronix}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ── WHAT TRONIXMESH PREVENTS ─────────────────────────────────── */}
      <section className="border-t border-gray-700 py-20 bg-gray-dark/30">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-white mb-4">What TronixMesh Prevents</h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              These are not hypothetical failure modes. They are enumerated halt triggers, tested and frozen in v1.0 doctrine.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {failureScenarios.map((s) => (
              <div key={s.title} className={`bg-gray-dark border ${s.color} rounded-lg p-6`}>
                <div className="text-3xl mb-3">{s.icon}</div>
                <h3 className="text-white font-bold mb-2">{s.title}</h3>
                <p className="text-gray-500 text-sm mb-3 leading-relaxed">{s.scenario}</p>
                <p className="text-gray-300 text-sm font-medium leading-relaxed">
                  <span className="text-blue font-bold">→ </span>{s.result}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CERTIFICATION TIERS ─────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-white mb-4">Certification Tiers</h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              TronixMesh compliance is verifiable and tiered. Deployments can demonstrate and display their governance level.
            </p>
          </div>
          <div className="grid md:grid-cols-4 gap-4">
            {certTiers.map((tier) => (
              <div key={tier.name} className="bg-gray-dark border border-gray-700 rounded-lg p-6 text-center hover:border-gray-500 transition-colors">
                <p className={`text-2xl font-black mb-1 ${tier.color}`}>{tier.name}</p>
                <p className="text-xs font-mono text-gray-600 mb-4">{tier.tag}</p>
                <p className="text-gray-400 text-sm leading-relaxed">{tier.desc}</p>
              </div>
            ))}
          </div>
          <p className="text-center text-gray-600 text-xs font-mono mt-6">Certification Profile v0.1 · 412 conformance tests · Details available under NDA</p>
        </div>
      </section>

      {/* ── PROOF POINTS ────────────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-16 bg-gray-dark/30">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { n: '412', label: 'Tests Passing', sub: 'Zero failures' },
              { n: '9', label: 'Doctrines Frozen', sub: 'v1.0 locked' },
              { n: '3', label: 'Patents Filed', sub: 'USPTO provisional' },
              { n: '7', label: 'Halt Triggers', sub: 'Enumerated & tested' },
            ].map(({ n, label, sub }) => (
              <div key={label} className="py-6">
                <p className="text-4xl font-black text-blue mb-1">{n}</p>
                <p className="text-sm font-bold text-white">{label}</p>
                <p className="text-xs text-gray-600 mt-1">{sub}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── WHO IT'S FOR ─────────────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-white mb-4">Who It's Built For</h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Any organization that needs to answer: what did the AI do, who authorized it, and can you prove it?
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: '🏗️',
                title: 'Construction & Field Ops',
                body: 'AI agents that authorize work, generate evidentiary documentation, and create records that hold up in court. State-coupled invalidation means altered records are provably altered.',
              },
              {
                icon: '🏥',
                title: 'Healthcare & Safety Systems',
                body: 'When AI assists in decisions affecting people\'s lives, you need a governance layer that proves what happened, who authorized it, and what the system was constitutionally permitted to do.',
              },
              {
                icon: '🏢',
                title: 'Enterprise AI Deployments',
                body: 'Deploy autonomous agents across your organization with confidence. Every action authorized. Every decision auditable. Every failure recoverable with a proof package.',
              },
            ].map(({ icon, title, body }) => (
              <div key={title} className="bg-gray-dark border border-gray-600 rounded-lg p-8 hover:border-blue transition-colors">
                <div className="text-4xl mb-4">{icon}</div>
                <h3 className="text-white font-bold mb-3">{title}</h3>
                <p className="text-gray-400 leading-relaxed text-sm">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ─────────────────────────────────────────────────────── */}
      <section className="border-t border-gray-700 py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-white mb-6">Ready to govern your AI?</h2>
          <p className="text-gray-400 text-lg mb-10 leading-relaxed">
            TronixMesh is in private deployment. We're working with enterprise builders, regulators, and strategic partners. Details available under NDA.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/architecture" className="px-8 py-4 border border-gray-600 text-gray-light font-semibold rounded hover:border-blue hover:text-blue transition">
              View Architecture
            </Link>
            <Link href="/contact" className="px-8 py-4 bg-blue text-white font-semibold rounded hover:bg-opacity-80 transition">
              Start a Conversation
            </Link>
          </div>
        </div>
      </section>

    </main>
  )
}
