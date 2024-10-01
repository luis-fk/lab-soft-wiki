import '@/styles/layout.css'
import Body from "@/components/Body";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
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
