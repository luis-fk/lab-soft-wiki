import '@/styles/layout/layout.css'
import Body from "@/components/layout/Body";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BackgroundImage from '@/components/layout/BackgroundImage';

export const metadata = {
  title: 'Wiki Dengue',
}

export default function InfoLayout({ children }) {
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
