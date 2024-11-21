import ArticleProvider from "./contexts/articleProvider"
import InfoProvider from "@/contexts/infoProvider"

export const metadata = {
  title: 'Wiki Dengue',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ArticleProvider>
          <InfoProvider>
            {children}
          </InfoProvider>
        </ArticleProvider>
      </body>
    </html>
  )
}
