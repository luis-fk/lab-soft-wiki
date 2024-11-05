import Body from "@/components/layout/Body";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import Welcome from "@/components/layout/Welcome";
import loremIpsum from "@/assets/json/loremIpsum.json";
import BackgroundImage from "@/components/layout/BackgroundImage";
import TrendingTopics from "@/components/layout/TrendingTopics";
import '@/styles/layout/backgroundImage.css'
import '@/styles/layout/layout.css'


export default function Page() {
  return (
    <>
      <BackgroundImage />

      <Header />

      <Body> 
        <TrendingTopics />
        <Welcome params={{title: "Bem vindo!", content: loremIpsum.lorem}} />
      </Body>

      <Footer />
    </>
  );
}
