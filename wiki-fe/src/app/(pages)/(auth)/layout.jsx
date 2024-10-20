import '@/styles/layout/layout.css'
import BackgroundImage from "@/app/_components/layout/BackgroundImage";

export const metadata = {
  title: 'Wiki Dengue',
}

export default function LoginLayout({ children }) {
  return (
    <html lang="en">
      <body>
          <BackgroundImage />
          
          {children}
      </body>
    </html>
  )
}
