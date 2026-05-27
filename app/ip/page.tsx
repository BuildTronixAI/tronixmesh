export default function IP() {
  return (
    <main className="min-h-screen">
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h1 className="text-white text-center mb-16">Intellectual Property</h1>

        <div className="max-w-3xl mx-auto space-y-12">
          <div className="p-12 bg-gray-dark border border-gray-600 rounded">
            <h2 className="text-blue text-2xl font-bold mb-4">Patent-Pending Architecture</h2>
            <div className="space-y-4 text-gray-400">
              <p>
                <strong className="text-white">Filed:</strong> May 2026
              </p>
              <p>
                <strong className="text-white">Inventor:</strong> Christopher C. Leiser
              </p>
              <p>
                <strong className="text-white">Status:</strong> Patent application under examination.
              </p>
            </div>
          </div>

          <div className="p-12 bg-gray-dark border border-gray-600 rounded">
            <h2 className="text-blue text-2xl font-bold mb-4">Licensing & Details</h2>
            <p className="text-gray-400 mb-6 leading-relaxed">
              Technical specifications, implementation details, and claims are protected under patent law. Full architecture documentation is available under executed NDA.
            </p>
            <p className="text-gray-400 leading-relaxed">
              We welcome inquiries from:
            </p>
            <ul className="text-gray-400 mt-4 space-y-2">
              <li>• Enterprise builders seeking governance infrastructure</li>
              <li>• Strategic investors evaluating defensible technology</li>
              <li>• Integration partners in regulated industries</li>
              <li>• Developers with relevant expertise</li>
            </ul>
          </div>

          <div className="p-12 bg-gray-dark border border-gray-600 rounded text-center">
            <h3 className="text-white mb-4">Get in Touch</h3>
            <p className="text-gray-400 mb-6">
              Ready to explore licensing, investment, or partnership opportunities?
            </p>
            <a href="/contact" className="inline-block px-8 py-3 bg-blue text-white rounded hover:bg-opacity-80 transition">
              Contact Us
            </a>
          </div>
        </div>
      </section>
    </main>
  )
}
