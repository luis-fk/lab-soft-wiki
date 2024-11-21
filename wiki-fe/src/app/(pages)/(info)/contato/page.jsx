'use client'
import React, { useEffect } from 'react';
import ContactForm from '@/components/info/ContactForm'
import Info from '@/components/info/Info'
import { infoIds } from "@/assets/misc/InfoIds";
import useFetchInfo from '@/hooks/fetchInfo';

export default function page() {
  const { info, errorMessage } = useFetchInfo(infoIds[4].getInContact);

  useEffect(() => {
    document.title = 'Entre em contato';
  }, []);

  return (
    <>
      <Info
        text={info?.text || 'Carregando...'}
        title={info?.title || 'Carregando...'}
        id={infoIds[4].getInContact}
        error={errorMessage}
      />
      <ContactForm />
    </>
  )
}
