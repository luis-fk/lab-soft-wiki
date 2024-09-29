import '@/styles/layout.css'
import Body from "@/components/Body";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata = {
  title: 'Wiki Dengue',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />

        <Body> 
          {children}
        </Body>

        <Footer />
      </body>
    </html>
  )
}
