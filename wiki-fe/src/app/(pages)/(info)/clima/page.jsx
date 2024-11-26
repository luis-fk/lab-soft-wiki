'use client'
import React, { useEffect, useState } from 'react';
import Weather from '@/app/_components/info/Weather';
import Info from '@/components/info/Info'
import { infoIds } from "@/assets/misc/InfoIds";
import useFetchInfo from '@/hooks/fetchInfo';

export default function Page() {
    const [forecast, setForecast] = useState(null);
    const [error, setError] = useState(null);

    const { info, errorMessage } = useFetchInfo(infoIds[3].effectOfTheRain);

    useEffect(() => {
        const fetchForecast = async () => {
            const lat = -20.8197;
            const lon = -49.3794;
            const url = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=4ebfebd6fb68c6041fef034307b03a9d&units=metric&lang=pt`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    setError('Failed to fetch forecast data');
                }
                const data = await response.json();
                const groupedData = groupByDay(data.list);
                setForecast(groupedData);
            } catch (err) {
                setError(err.message);
                console.error("Error fetching weather data:", err);
            }
        };

        fetchForecast();
    }, []);

    const groupByDay = (list) => {
        return list.reduce((acc, entry) => {
            const date = new Date(entry.dt_txt).toLocaleDateString('pt-BR', {
                weekday: 'long',
                day: 'numeric',
                month: 'short'
            });
            if (!acc[date]) {
                acc[date] = [];
            }
            acc[date].push(entry);
            return acc;
        }, {});
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-start' }}>
            <Weather forecast={forecast} error={error}/>

            <Info
                text={info?.text || 'Carregando...'}
                title={info?.title || 'Carregando...'}
                id={infoIds[3].effectOfTheRain}
                error={errorMessage}
            />
        </div>
    );
}
