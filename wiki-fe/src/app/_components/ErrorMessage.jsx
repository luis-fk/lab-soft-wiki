import React from 'react';
import '@/styles/errorMessage.css';
import Content from './Content';
import lorem from '@/assets/json/loremIpsum.json';

export default function ErrorMessage({ message }) {
    return (
        <>
            {message && (
                <div className="error-message">
                    {message}
                </div>
            )}
        </>
    );
}
