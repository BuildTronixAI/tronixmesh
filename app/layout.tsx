import type { Metadata } from 'next'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'TronixMesh - Governance Architecture for Autonomous Systems',
  description: 'The infrastructure layer the industry doesn\'t know it needs yet. Patent-pending governance architecture for autonomous systems in regulated industries.',
  openGraph: {
    title: 'TronixMesh',
    description: 'Governance architecture for autonomous systems. Patent pending.',
    url: 'https://tronixmesh.com',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-navy text-white">
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  )
}
