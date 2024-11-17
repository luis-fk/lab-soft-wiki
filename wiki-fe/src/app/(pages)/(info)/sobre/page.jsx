'use client'
import React, { useEffect } from 'react';
import Info from '@/components/info/Info'
import { infoIds } from "@/assets/misc/InfoIds";
import useFetchInfo from '@/hooks/fetchInfo';

export default function page() {
  const { info, errorMessage } = useFetchInfo(infoIds[1].aboutTheProject);

  useEffect(() => {
    document.title = 'Sobre o projeto';
  }, []);

  return (
    <Info
      text={info?.text || 'Carregando...'}
      title={info?.title || 'Carregando...'}
      id={infoIds[1].aboutTheProject}
      error={errorMessage}
    />
  )
}
