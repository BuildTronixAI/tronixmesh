'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="border-b border-gray-700 sticky top-0 z-50 bg-navy bg-opacity-95 backdrop-blur">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-blue">
          TronixMesh
        </Link>
        
        <nav className="hidden md:flex gap-8 items-center">
          <Link href="/" className="text-gray-light hover:text-blue transition">Home</Link>
          <Link href="/architecture" className="text-gray-light hover:text-blue transition">Architecture</Link>
          <Link href="/constitution" className="text-gray-light hover:text-blue transition">Commandments</Link>
          <Link href="/ip" className="text-gray-light hover:text-blue transition">IP</Link>
          <Link href="/contact" className="px-6 py-2 bg-blue text-white rounded hover:bg-opacity-80 transition">Contact</Link>
        </nav>

        <button 
          className="md:hidden text-gray-light"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          ☰
        </button>

        {mobileMenuOpen && (
          <nav className="absolute top-16 left-0 right-0 bg-gray-dark md:hidden flex flex-col gap-4 p-6 border-b border-gray-700">
            <Link href="/" className="text-gray-light hover:text-blue">Home</Link>
            <Link href="/architecture" className="text-gray-light hover:text-blue">Architecture</Link>
            <Link href="/constitution" className="text-gray-light hover:text-blue">Commandments</Link>
            <Link href="/ip" className="text-gray-light hover:text-blue">IP</Link>
            <Link href="/contact" className="text-gray-light hover:text-blue">Contact</Link>
          </nav>
        )}
      </div>
    </header>
  )
}
