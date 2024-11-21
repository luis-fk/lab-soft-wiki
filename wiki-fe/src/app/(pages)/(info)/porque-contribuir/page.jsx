'use client'
import React, { useEffect } from 'react';
import Info from '@/components/info/Info'
import { infoIds } from "@/assets/misc/InfoIds";
import useFetchInfo from '@/hooks/fetchInfo';

export default function page() {
  const { info, errorMessage } = useFetchInfo(infoIds[2].howToHelp);

  useEffect(() => {
    document.title = 'Porque contribuir?';
  }, []);

  return (
    <Info
      text={info?.text || 'Carregando...'}
      title={info?.title || 'Carregando...'}
      id={infoIds[2].howToHelp}
      error={errorMessage}
    />
  )
}
