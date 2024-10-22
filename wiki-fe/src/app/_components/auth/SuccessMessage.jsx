import React from 'react';
import '@/styles/auth/successMessage.css';

export default function SuccessMessage({ message }) {
    return (
        <>
            {message && (
                <div className="success-message">
                    {message}
                </div>
            )}
        </>
    );
}
