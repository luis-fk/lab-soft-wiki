'use client';
import React, { useEffect } from 'react';
import useFetchImage from '@/hooks/fetchImage';
import ErrorMessage from '@/components/auth/ErrorMessage';
import "@/styles/info/epidemiological-data.css";

const IMAGES = [
  { key: 'notWorked', url: 'http://localhost:8000/mapa/nao-trabalhados/', alt: 'Mapa de dados imóveis não trabalhados' },
  { key: 'incidency', url: 'http://localhost:8000/mapa/incidencia-aedes/', alt: 'Mapa de incidência de mosquitos' },
  { key: 'treated', url: 'http://localhost:8000/mapa/tratamento-imoveis/', alt: 'Mapa de imóveis tratados' },
];

export default function Page() {
  const fetchedImages = IMAGES.map(({ key, url }) => {
    const { imageSrc, errorMessage } = useFetchImage(url);
    return { key, imageSrc, errorMessage };
  });

  useEffect(() => {
    document.title = 'Dados epidemiológicos';
  }, []);

  const hasErrors = fetchedImages.some(({ errorMessage }) => errorMessage);
  const firstErrorMessage = fetchedImages.find(({ errorMessage }) => errorMessage)?.errorMessage;

  if (hasErrors) {
    return <ErrorMessage message={firstErrorMessage} />;
  }

  return (
    <div className="data-container">
      {fetchedImages.map(({ key, imageSrc, alt }) => (
        imageSrc ? <img key={key} src={imageSrc} alt={alt} /> : <div key={key}>Loading...</div>
      ))}
    </div>
  );
}
