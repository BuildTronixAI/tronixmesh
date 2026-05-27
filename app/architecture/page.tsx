export default function Architecture() {
  const planes = [
    {
      name: 'Identity',
      description: 'Cryptographic attribution and provenance for every autonomous action.'
    },
    {
      name: 'Control',
      description: 'Real-time governance policies that enforce compliance constraints at runtime.'
    },
    {
      name: 'Data',
      description: 'Immutable audit trail and state verification for decision transparency.'
    },
    {
      name: 'Sync',
      description: 'Distributed consensus for multi-agent coordination across system boundaries.'
    },
    {
      name: 'Audit',
      description: 'Continuous monitoring and attestation for regulatory compliance reporting.'
    }
  ]

  return (
    <main className="min-h-screen">
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h1 className="text-white text-center mb-4">Architecture</h1>
        <p className="text-gray-400 text-center max-w-2xl mx-auto mb-16 text-lg">
          Five planes of governance. Built from the ground up for autonomous systems.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {planes.map((plane, idx) => (
            <div 
              key={idx}
              className="bg-gray-dark border border-gray-600 rounded p-8 hover:border-blue transition hover:shadow-lg hover:shadow-blue"
            >
              <h3 className="text-blue text-2xl font-bold mb-4">{plane.name}</h3>
              <p className="text-gray-400 leading-relaxed">{plane.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-20 p-12 bg-gray-dark border border-gray-600 rounded">
          <h2 className="text-white mb-6">Integration-Ready</h2>
          <p className="text-gray-400 leading-relaxed mb-4">
            These planes integrate with your existing systems. APIs for AI agents, robotics platforms, sensor networks, and legacy control systems. Enterprise-grade governance without replacing your infrastructure.
          </p>
          <p className="text-gray-400 leading-relaxed">
            Details available under NDA. <a href="/contact" className="text-blue font-semibold">Let's talk.</a>
          </p>
        </div>
      </section>
    </main>
  )
}
