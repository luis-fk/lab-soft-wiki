import Body from "@/components/Body";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Content from "@/components/Content";
import loremIpsum from "@/assets/json/loremIpsum.json";
import BackgroundImage from "@/components/BackgroundImage";
import '@/styles/backgroundImage.css'
import '@/styles/layout.css'


export default function Page() {
  return (
    <>
      <BackgroundImage />

      <Header />

      <Body> 
        <Content params={{title: "Bem vindo!", content: loremIpsum.lorem}} />
      </Body>

      <Footer />
    </>
  );
}
