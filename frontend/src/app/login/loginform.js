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
            const response = await fetch('http://localhost:8080/auth/login', {
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
            console.log('Login successful, token:', data.token);
            router.push('/dashboard');
        } catch (error) {
            setError('An error occurred during login');
            console.error('An error occurred during login:', error);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen ">
            <div className="flex flex-col pt-5 pb-32 min-h-[632px] min-w-[240px] w-[512px] bg-white rounded-xl max-md:pb-24"> {/* Add shadow and rounded corners */}
                <h2 className="flex flex-col justify-center items-start p-4 w-full text-3xl font-bold tracking-tighter leading-none text-black whitespace-nowrap">
                    Login
                </h2>
                <form onSubmit={handleLogin}>
                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="email" className="pb-2 w-full font-medium text-stone-900">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your email"
                            required

                        />
                    </div>

                    <div className="flex flex-col px-4 py-3 w-full text-base">
                        <label htmlFor="password" className="pb-2 w-full font-medium text-stone-900">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="p-4 bg-lime-50 rounded-xl w-full min-h-[56px]"
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    {error && (
                        <div className="text-red-500 text-center py-2">{error}</div>
                    )}

                    <div className="px-4 py-3 w-full">
                        <button
                            type="submit"
                            className="w-full px-5 py-3 bg-emerald-600 text-white font-bold rounded-3xl"
                        >
                            Login
                        </button>
                    </div>
                </form>
                <div className="flex justify-center items-center w-full py-4">
                    <p className="text-base text-gray-600">
                        Don’t have an account?{' '}
                        <Link href="/register" className="text-blue-600 font-bold hover:underline">
                            Register now
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default LoginForm;
