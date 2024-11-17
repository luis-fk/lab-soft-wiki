import React from 'react';
import { Card, CardContent, Typography, Grid, Box, Divider } from '@mui/material';

export default function Weather({ forecast, error }) {
  return (
    <Box sx={{ paddingLeft: 5, paddingRight: 5, width: '70%', paddingBottom: 2 }}>
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
  )
}
