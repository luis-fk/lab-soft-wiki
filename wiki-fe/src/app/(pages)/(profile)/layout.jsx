import '@/styles/layout/layout.css'
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import ProfileBody from "@/components/profile/Body";
import BackgroundImage from '@/app/_components/layout/BackgroundImage';

export const metadata = {
  title: 'Wiki Dengue',
}

export default function ProfileLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <BackgroundImage />
        
        <Header />

        <ProfileBody> 
          {children}
        </ProfileBody>

        <Footer />
      </body>
    </html>
  )
}
