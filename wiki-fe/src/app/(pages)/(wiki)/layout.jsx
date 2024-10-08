import '@/styles/layout.css'
import Body from "@/app/_components/layout/Body";
import Header from "@/app/_components/layout/Header";
import Footer from "@/app/_components/layout/Footer";
import BackgroundImage from '@/app/_components/BackgroundImage';

export const metadata = {
  title: 'Wiki Dengue',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <BackgroundImage />
        
        <Header />

        <Body> 
          {children}
        </Body>

        <Footer />
      </body>
    </html>
  )
}
