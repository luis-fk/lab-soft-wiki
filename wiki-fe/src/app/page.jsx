import Body from "@/app/_components/layout/Body";
import Header from "@/app/_components/layout/Header";
import Footer from "@/app/_components/layout/Footer";
import Content from "@/app/_components/layout/Content";
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
