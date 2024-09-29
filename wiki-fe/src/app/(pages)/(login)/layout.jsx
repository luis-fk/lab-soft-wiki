import '@/styles/layout.css'

export const metadata = {
  title: 'Wiki Dengue',
}

export default function LoginLayout({ children }) {
  return (
    <html lang="en">
      <body>
          {children}
      </body>
    </html>
  )
}
