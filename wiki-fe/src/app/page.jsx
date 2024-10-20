import Body from "@/components/layout/Body";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import Article from "@/components/layout/Article";
import loremIpsum from "@/assets/json/loremIpsum.json";
import BackgroundImage from "@/components/BackgroundImage";
import '@/styles/layout/backgroundImage.css'
import '@/styles/layout/layout.css'


export default function Page() {
  return (
    <>
      <BackgroundImage />

      <Header />

      <Body> 
        <Article params={{title: "Bem vindo!", content: loremIpsum.lorem}} />
      </Body>

      <Footer />
    </>
  );
}
