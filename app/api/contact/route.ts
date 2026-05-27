import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { name, company, email, interest, message } = body

    // Validate required fields
    if (!name || !company || !email || !interest) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Simple in-memory log for now
    // In production, you'd store this in a database or send an email
    console.log('Contact form submission:', {
      name,
      company,
      email,
      interest,
      message,
      timestamp: new Date().toISOString()
    })

    return NextResponse.json(
      { success: true, message: 'Contact request received' },
      { status: 200 }
    )
  } catch (error) {
    console.error('Contact form error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
