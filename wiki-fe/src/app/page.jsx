import Content from "@/components/Content";
import loremIpsum from "@/assets/json/loremIpsum.json";

export default function Page() {
  return (
    <Content params={{title: "Bem vindo!", content: loremIpsum.lorem}} />
  );
}
