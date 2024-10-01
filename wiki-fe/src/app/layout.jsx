import '@/styles/layout.css'
import BackgroundImage from "@/components/BackgroundImage";

export const metadata = {
  title: 'Wiki Dengue',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
          <BackgroundImage />

          {children}
      </body>
    </html>
  )
}
