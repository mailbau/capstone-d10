"use client";

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

function LoginForm() {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [error, setError] = React.useState('');
    const router = useRouter();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            // const response = await fetch('http://localhost:8080/auth/login', {
            const response = await fetch('https://capstoned10.duckdns.org//auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                setError(errorData.message);
                return;
            }

            const data = await response.json();
            localStorage.setItem('token', data.token);
            router.push('/dashboard');
        } catch (error) {
            setError('An error occurred during login');
            console.error('An error occurred during login:', error);
        }
    };

    return (
        <div className="flex justify-center items-center w-full">
            <div className="flex flex-col w-full max-w-md bg-white rounded-2xl shadow-lg p-8 space-y-6">
                <h2 className="text-3xl font-bold text-center text-gray-800">
                    Welcome Back!
                </h2>
                <p className="text-gray-600 text-center">
                    Log in to continue managing waste efficiently
                </p>

                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="flex flex-col">
                        <label htmlFor="email" className="text-gray-700 font-medium mb-1">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="password" className="text-gray-700 font-medium mb-1">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    {error && (
                        <div className="text-red-500 text-center">{error}</div>
                    )}

                    <button
                        type="submit"
                        className="w-full py-3 bg-emerald-600 text-white font-bold rounded-full shadow-md hover:bg-emerald-700 transition"
                    >
                        Login
                    </button>
                </form>

                <div className="text-center">
                    <p className="text-gray-600">
                        Don’t have an account?{' '}
                        <Link href="/register" className="text-blue-600 font-semibold hover:underline">
                            Register now
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default LoginForm;
