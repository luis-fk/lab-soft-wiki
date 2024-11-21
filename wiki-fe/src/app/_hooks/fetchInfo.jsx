'use client'
import { useState, useEffect } from 'react';

const useFetchInfo = (infoId) => {
    const [info, setInfo] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        const fetchInfo = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/siteinfo/?id=${infoId}`);
                if (!response.ok) {
                    setErrorMessage("Ocorreu um erro ao buscar as informações!");
                }
                const data = await response.json();
                setInfo(data);
            } catch (error) {
                setErrorMessage("Ocorreu um erro ao carregar a informação!");
            }
        };

        fetchInfo();
    }, [infoId]);

    return { info, errorMessage };
};

export default useFetchInfo;
