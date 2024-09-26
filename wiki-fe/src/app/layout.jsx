import '@/styles/layout.css'
import Body from "@/components/Body";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Content from "@/components/Content";


export const metadata = {
  title: 'Next.js',
  description: 'Generated by Next.js',
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
