import React from 'react';
import '@/styles/auth/errorMessage.css';

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
