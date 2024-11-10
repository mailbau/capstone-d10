"use client";

import React, { useState } from 'react';
import Link from 'next/link';

function RegisterForm() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = {
            first_name: firstName,
            last_name: lastName,
            user_email: email,
            user_password: password
        };

        try {
            // const response = await fetch('http://localhost:8080/user/register', {
            const response = await fetch('https://capstoned10.duckdns.org/user/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess(data.message || 'Registration successful!');
                setError('');
                setFirstName('');
                setLastName('');
                setEmail('');
                setPassword('');
            } else {
                setError(data.error || 'Registration failed. Please try again.');
                setSuccess('');
            }
        } catch (error) {
            setError('Network error. Please try again later.');
            setSuccess('');
        }
    };

    return (
        <div className="flex justify-center items-center w-full">
            <div className="flex flex-col w-full max-w-md bg-white rounded-2xl shadow-lg p-8 space-y-6">
                <h2 className="text-3xl font-bold text-center text-gray-800">
                    Create an Account
                </h2>
                <p className="text-gray-600 text-center">
                    Join us and start managing waste efficiently
                </p>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex flex-col">
                        <label htmlFor="firstName" className="text-gray-700 font-medium mb-1">
                            First Name
                        </label>
                        <input
                            type="text"
                            id="firstName"
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your first name"
                            value={firstName}
                            onChange={(e) => setFirstName(e.target.value)}
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="lastName" className="text-gray-700 font-medium mb-1">
                            Last Name
                        </label>
                        <input
                            type="text"
                            id="lastName"
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your last name"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="email" className="text-gray-700 font-medium mb-1">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
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
                            className="p-3 bg-gray-100 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-emerald-500 outline-none transition"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-3 bg-emerald-600 text-white font-bold rounded-full shadow-md hover:bg-emerald-700 transition"
                    >
                        Register
                    </button>
                </form>

                {error && <p className="text-red-500 text-center mt-2">{error}</p>}
                {success && <p className="text-green-500 text-center mt-2">{success}</p>}

                <div className="text-center">
                    <p className="text-gray-600">
                        Already have an account?{' '}
                        <Link href="/login" className="text-blue-600 font-semibold hover:underline">
                            Login
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default RegisterForm;
