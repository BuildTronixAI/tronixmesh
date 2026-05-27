'use client'

import { useState } from 'react'

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    interest: 'Licensing',
    message: ''
  })
  
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const interestOptions = ['Licensing', 'Investment', 'Partnership', 'Developer Access']

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        setSubmitted(true)
        setFormData({ name: '', company: '', email: '', interest: 'Licensing', message: '' })
        setTimeout(() => setSubmitted(false), 5000)
      }
    } catch (error) {
      console.error('Error submitting form:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen">
      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-12">
          <h1 className="text-white mb-4">Get in Touch</h1>
          <p className="text-gray-400 text-lg">
            If you're building autonomous systems at scale in regulated industries — let's talk.
          </p>
        </div>

        <div className="bg-gray-dark border border-gray-600 rounded p-8 md:p-12">
          {submitted ? (
            <div className="text-center py-12">
              <h2 className="text-white text-2xl font-bold mb-4">Thank You</h2>
              <p className="text-gray-400 mb-2">We've received your inquiry.</p>
              <p className="text-gray-400">Our team will be in touch shortly.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-white font-semibold mb-2">
                  Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  placeholder="Your full name"
                  className="w-full"
                />
              </div>

              <div>
                <label htmlFor="company" className="block text-white font-semibold mb-2">
                  Company *
                </label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  required
                  placeholder="Your company name"
                  className="w-full"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-white font-semibold mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  placeholder="your@email.com"
                  className="w-full"
                />
              </div>

              <div>
                <label htmlFor="interest" className="block text-white font-semibold mb-2">
                  Interest *
                </label>
                <select
                  id="interest"
                  name="interest"
                  value={formData.interest}
                  onChange={handleChange}
                  className="w-full"
                >
                  {interestOptions.map(option => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="message" className="block text-white font-semibold mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Tell us about your needs..."
                  rows={6}
                  className="w-full"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue text-white font-semibold py-3 rounded hover:bg-opacity-80 transition disabled:opacity-50"
              >
                {loading ? 'Sending...' : 'Send Message'}
              </button>
            </form>
          )}
        </div>

        <div className="mt-12 text-center text-gray-400">
          <p>Or reach out directly: <a href="mailto:contact@tronixmesh.com" className="text-blue">contact@tronixmesh.com</a></p>
        </div>
      </section>
    </main>
  )
}
