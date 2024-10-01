"use client"
import React, { useState } from 'react';
import "@/styles/login.css";

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
    event.preventDefault();
        try {
        await fetch('http://127.0.0.1:8000/user/logar/', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
            username,
            password,
            email,
            }), 
        });
        } catch (error) {
        console.log(error);
        }
    };

    return (
    <>
        <div className="signup-container">
            <h2>Entrar</h2>
            <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="password">Senha</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                <div className="submitButton-container">
                    <button type="submit">Entrar</button>
                </div>
            </form>
        </div>
    </>
    )
}
