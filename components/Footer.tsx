export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-gray-700 bg-navy mt-20 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-blue font-bold mb-4">TronixMesh</h3>
            <p className="text-sm text-gray-400">
              Governance architecture for autonomous systems in regulated industries.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="/architecture" className="hover:text-blue transition">Architecture</a></li>
              <li><a href="/ip" className="hover:text-blue transition">Patents</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="/contact" className="hover:text-blue transition">Contact</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 text-center text-sm text-gray-500">
          <p>&copy; {currentYear} TronixMesh. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
