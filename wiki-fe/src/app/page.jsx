'use client'
import Info from '@/components/info/Info'
import Body from "@/components/layout/Body";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import useFetchInfo from '@/hooks/fetchInfo';
import BackgroundImage from "@/components/layout/BackgroundImage";
import TrendingTopics from "@/components/layout/TrendingTopics";
import { infoIds } from "@/assets/misc/InfoIds";
import React, { useEffect } from 'react';
import '@/styles/layout/backgroundImage.css'
import '@/styles/layout/layout.css'

export default function Page() {
  const { info, errorMessage } = useFetchInfo(infoIds[5].welcome);

  useEffect(() => {
    document.title = 'Wiki Dengue';
  }, []);

  return (
    <>
      <BackgroundImage />

      <Header />

      <Body> 
        <TrendingTopics />
        <Info
          text={info?.text || 'Carregando...'}
          title={info?.title || 'Carregando...'}
          id={infoIds[5].welcome}
          error={errorMessage}
        />
      </Body>

      <Footer />
    </>
  );
}
