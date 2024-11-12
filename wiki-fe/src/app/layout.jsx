import ArticleProvider from "./contexts/articleProvider"

export const metadata = {
  title: 'Wiki Dengue',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ArticleProvider>
          {children}
        </ArticleProvider>
      </body>
    </html>
  )
}
