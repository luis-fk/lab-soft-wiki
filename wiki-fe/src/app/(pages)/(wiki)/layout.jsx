import '@/styles/layout/layout.css'
import Body from "@/components/layout/Body";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BackgroundImage from '@/components/layout/BackgroundImage';

// import para o uso do provider
import ArticleProvider from '@/app/contexts/articleProvider';

export const metadata = {
  title: 'Wiki Dengue',
}

export default function WikiLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <BackgroundImage />
        
        <Header />
        {/* ArticleProvider recebe todos os parametros de children */}
        <ArticleProvider> 
          <Body> 
            {children}
          </Body>
        </ArticleProvider>

        <Footer />
      </body>
    </html>
  )
}
