import Link from 'next/link'

export default function Home() {
  const audiences = [
    {
      title: 'Builders',
      description: 'Scale autonomous systems with governance that meets regulatory requirements. No more jury-rigged compliance layers.',
      icon: '⚙️'
    },
    {
      title: 'Investors',
      description: 'Patent-pending infrastructure. Real defensibility. Real moat. Deployed in regulated industries.',
      icon: '🔐'
    },
    {
      title: 'Partners',
      description: 'Integration framework for AI agents, robotics, sensors. Enterprise-grade governance at the infrastructure layer.',
      icon: '🤝'
    }
  ]

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
        <div className="text-center">
          <h1 className="text-white mb-6">
            The infrastructure layer the industry doesn't know it needs yet
          </h1>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto leading-relaxed">
            Governance architecture for autonomous systems. Patent pending.
            <br />
            Built for regulated industries. Designed for scale.
          </p>
          <Link href="/contact">
            <button className="px-8 py-3 bg-blue text-white font-semibold rounded hover:bg-opacity-80 transition">
              Start a Conversation
            </button>
          </Link>
        </div>
      </section>

      {/* Audience Cards */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {audiences.map((audience, idx) => (
            <div key={idx} className="bg-gray-dark border border-gray-600 rounded p-8 hover:border-blue transition">
              <div className="text-4xl mb-4">{audience.icon}</div>
              <h3 className="text-white mb-4">{audience.title}</h3>
              <p className="text-gray-400 leading-relaxed">{audience.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 border-t border-gray-700">
        <div className="text-center">
          <h2 className="text-white mb-6">Ready to explore?</h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto text-lg">
            If you're building autonomous systems at scale in regulated industries, let's talk.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/architecture">
              <button className="px-8 py-3 border border-blue text-blue rounded hover:bg-blue hover:text-white transition">
                View Architecture
              </button>
            </Link>
            <Link href="/contact">
              <button className="px-8 py-3 bg-blue text-white rounded hover:bg-opacity-80 transition">
                Get in Touch
              </button>
            </Link>
          </div>
        </div>
      </section>
    </main>
  )
}
