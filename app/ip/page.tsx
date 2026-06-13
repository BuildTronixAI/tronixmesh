export default function IP() {
  const patents = [
    {
      id: 'TM-PAT-0001',
      num: '64/072,487',
      title: 'System and Method for Cryptographic Governance Enforcement in Multi-Agent AI Systems',
      filed: 'May 22, 2026',
      status: 'Filed',
      covers: 'Key lifecycle management, nonce-based replay prevention, Ed25519 audit chain, quorum enforcement, halt/recovery state machine.',
    },
    {
      id: 'TM-PAT-0002',
      num: '64/073,859',
      title: 'System and Method for Composing Multiple Autonomous Agents into a Governed Collective Intelligence via a Central Governance Substrate',
      filed: 'May 25, 2026',
      status: 'Filed',
      covers: 'Multi-agent composition, sovereign governance state, Control Plane authority, distinct-owner quorum, UNTRUSTED terminality.',
    },
    {
      id: 'TM-PAT-0003',
      num: 'Filing imminent',
      title: 'System and Method for Cryptographic Governance Authority Migration to an Isolated Degraded Execution Plane in Governed Multi-Agent AI Systems',
      filed: 'Imminent',
      status: 'Imminent',
      covers: 'Degraded Execution Plane (DEP), cryptographic plane independence, Q_DEP ≥ Q_MAIN + ⌈M/4⌉, exit proof re-entry gate, UNTRUSTED terminal state.',
    },
  ]

  return (
    <main className="min-h-screen">
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h1 className="text-white mb-4">Intellectual Property</h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Three-patent portfolio covering cryptographic governance enforcement, governed collective intelligence, and fault plane isolation for autonomous AI systems.
          </p>
        </div>

        {/* Patent table */}
        <div className="space-y-6 mb-16">
          {patents.map((p) => (
            <div key={p.id} className="p-8 bg-gray-dark border border-gray-600 rounded-lg hover:border-blue transition-colors">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <span className="text-xs font-mono text-blue">{p.id}</span>
                  {p.num !== 'Filing imminent' && (
                    <span className="text-xs font-mono text-gray-500 ml-3">No. {p.num}</span>
                  )}
                </div>
                <span className={`text-xs font-mono border rounded px-2 py-0.5 shrink-0 ${
                  p.status === 'Filed'
                    ? 'text-cyan-400 border-cyan-400/30 bg-cyan-400/5'
                    : 'text-amber-400 border-amber-400/30 bg-amber-400/5'
                }`}>
                  {p.status}
                </span>
              </div>
              <h3 className="text-white font-semibold mb-3 leading-tight">{p.title}</h3>
              <p className="text-gray-500 text-sm mb-2"><strong className="text-gray-400">Filed:</strong> {p.filed}</p>
              <p className="text-gray-500 text-sm"><strong className="text-gray-400">Covers:</strong> {p.covers}</p>
            </div>
          ))}
        </div>

        {/* Inventor */}
        <div className="p-8 bg-gray-dark border border-gray-600 rounded-lg mb-8">
          <h2 className="text-blue text-xl font-bold mb-4">Inventor</h2>
          <div className="space-y-2 text-gray-400 text-sm">
            <p><strong className="text-white">Name:</strong> Christopher Channing Leiser</p>
            <p><strong className="text-white">Location:</strong> Key West, Florida</p>
            <p><strong className="text-white">Priority dates:</strong> May 22, 2026 · May 25, 2026</p>
            <p><strong className="text-white">Assignee:</strong> L2R Holdings LLC</p>
          </div>
        </div>

        {/* Licensing */}
        <div className="p-8 bg-gray-dark border border-gray-600 rounded-lg mb-8">
          <h2 className="text-blue text-xl font-bold mb-4">Licensing & Details</h2>
          <p className="text-gray-400 leading-relaxed mb-4">
            Technical specifications, implementation details, and claims are protected under patent law. Full architecture documentation is available under executed NDA.
          </p>
          <p className="text-gray-400 leading-relaxed mb-4">We welcome inquiries from:</p>
          <ul className="text-gray-400 space-y-2 text-sm">
            <li>• Enterprise builders seeking governance infrastructure</li>
            <li>• Strategic investors evaluating defensible technology</li>
            <li>• Integration partners in regulated industries</li>
            <li>• AI platform developers requiring compliance layers</li>
          </ul>
        </div>

        <div className="p-8 bg-gray-dark border border-gray-600 rounded-lg text-center">
          <h3 className="text-white mb-4">Get in Touch</h3>
          <p className="text-gray-400 mb-6">
            Ready to explore licensing, investment, or partnership opportunities?
          </p>
          <a href="/contact" className="inline-block px-8 py-3 bg-blue text-white rounded hover:bg-opacity-80 transition font-semibold">
            Contact Us
          </a>
        </div>
      </section>
    </main>
  )
}
