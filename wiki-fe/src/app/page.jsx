import Content from "@/components/Content";
import loremIpsum from "@/assets/json/loremIpsum.json";
import Body from "@/components/Body";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function Page() {
  return (
    <>
      <Header />

      <Body> 
        <Content params={{title: "Bem vindo!", content: loremIpsum.lorem}} />
      </Body>

      <Footer />
    </>
  );
}
