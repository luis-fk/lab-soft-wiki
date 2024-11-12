'use client'
import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, Divider } from '@mui/material';

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

    // Helper function to group forecast data by day
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
        <Box sx={{ paddingLeft: 40, paddingRight: 40, paddingBottom: 2 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Temperatura nos próximo 5 dias
            </Typography>
            {error ? (
                <Typography color="error">Error: {error}</Typography>
            ) : forecast ? (
                <Grid container spacing={2}>
                    {Object.entries(forecast).map(([day, entries], index) => (
                        <Grid item xs={12} key={index}>
                            <Card sx={{ backgroundColor: '#f5f5f5', borderRadius: 2 }}>
                                <CardContent>
                                    <Typography variant="h5" gutterBottom>
                                        {day.charAt(0).toUpperCase() + day.slice(1)}
                                    </Typography>
                                    {/* Header Row */}
                                    <Grid container sx={{ marginBottom: 1, fontWeight: 'bold' }}>
                                        <Grid item xs={4}>
                                            <Typography variant="body2">Horário</Typography>
                                        </Grid>
                                        <Grid item xs={4} sx={{ textAlign: 'center' }}>
                                            <Typography variant="body2">Temperatura</Typography>
                                        </Grid>
                                        <Grid item xs={4} sx={{ textAlign: 'right' }}>
                                            <Typography variant="body2">Descrição</Typography>
                                        </Grid>
                                    </Grid>
                                    <Divider />
                                    {/* Forecast Rows */}
                                    {entries.map((entry, idx) => (
                                        <Box key={idx}>
                                            <Grid container alignItems="center" sx={{ paddingY: 0.5 }}>
                                                <Grid item xs={4}>
                                                    <Typography variant="body2">
                                                        {new Date(entry.dt_txt).toLocaleTimeString('pt-BR', {
                                                            hour: '2-digit',
                                                            minute: '2-digit'
                                                        })}
                                                    </Typography>
                                                </Grid>
                                                <Grid item xs={4} sx={{ textAlign: 'center' }}>
                                                    <Typography variant="body2">
                                                    {Math.trunc(entry.main.temp)} °C
                                                    </Typography>
                                                </Grid>
                                                <Grid item xs={4} sx={{ textAlign: 'right', display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                                                    <Typography variant="body2" sx={{ marginRight: 1 }}>
                                                        {entry.weather[0].description.charAt(0).toUpperCase() + entry.weather[0].description.slice(1)}
                                                    </Typography>
                                                    <img 
                                                        src={`https://openweathermap.org/img/wn/${entry.weather[0].icon}@2x.png`} 
                                                        alt={entry.weather[0].description} 
                                                        width="30" 
                                                        height="30"
                                                    />
                                                </Grid>
                                            </Grid>
                                        </Box>
                                    ))}
                                    <Divider sx={{ marginTop: 2 }} />
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            ) : (
                <Typography>Loading forecast...</Typography>
            )}
        </Box>
    );
}
