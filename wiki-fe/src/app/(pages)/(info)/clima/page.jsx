'use client'
import React, { useEffect, useState } from 'react';
import Weather from '@/app/_components/info/Weather';

export default function Page() {
    const [forecast, setForecast] = useState(null);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const fetchForecast = async () => {
            const lat = -20.8197;
            const lon = -49.3794;
            const url = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${process.env.NEXT_PUBLIC_OPENWEATHER_API_KEY}&units=metric&lang=pt`;


            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Failed to fetch forecast data');
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
        <Weather forecast={forecast} error={error}/>
    );
}
