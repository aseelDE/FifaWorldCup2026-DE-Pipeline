import './globals.css'

export const metadata = {
  title: 'FIFA World Cup 2026 | Data Pipeline',
  description: 'Real-time FIFA World Cup 2026 analytics powered by a full data engineering pipeline',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;600&display=swap" rel="stylesheet" />
      </head>
      <body>{children}</body>
    </html>
  )
}