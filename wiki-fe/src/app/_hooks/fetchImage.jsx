'use client';
import { useState, useEffect } from 'react';

const useFetchImage = (url) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await fetch(url, { method: 'GET' });
        if (!response.ok) {
            setErrorMessage('Ocorreu um erro ao carregar a imagem!');
        }

        const blob = await response.blob(); 
        const imageURL = URL.createObjectURL(blob); 
        setImageSrc(imageURL);
      } catch (error) {
        setErrorMessage('Ocorreu um erro ao carregar a imagem!');
      }
    };

    fetchImage();
  }, [url]);

  return { imageSrc, errorMessage };
};

export default useFetchImage;
