// File: pages/Settings.js
"use client";

import React, { useState } from 'react';
import Header from '../../components/header';
import Footer from '../../components/footer';

function Settings() {
    const [notificationsEnabled, setNotificationsEnabled] = useState(false);
    const [theme, setTheme] = useState('light');

    const handleSaveSettings = () => {
        alert('Settings saved successfully!');
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex flex-col items-center justify-center flex-grow w-full p-6">
                <div className="flex flex-col items-center w-full max-w-2xl p-6 space-y-6 bg-white rounded-lg shadow-lg">
                    <div className="flex flex-col items-center w-full mb-6">
                        <h2 className="text-3xl font-bold text-gray-800">Settings</h2>
                        <p className="mt-2 text-gray-500">Customize your preferences</p>
                    </div>
                    <div className="flex flex-col space-y-4 w-full">
                        <div className="flex items-center justify-between">
                            <label className="text-gray-800 font-medium">Enable Notifications</label>
                            <input
                                type="checkbox"
                                checked={notificationsEnabled}
                                onChange={() => setNotificationsEnabled(!notificationsEnabled)}
                                className="form-checkbox h-5 w-5 text-blue-600"
                            />
                        </div>
                        <div className="flex flex-col space-y-2">
                            <label className="text-gray-800 font-medium">Select Theme</label>
                            <select
                                value={theme}
                                onChange={(e) => setTheme(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="light">Light</option>
                                <option value="dark">Dark</option>
                            </select>
                        </div>
                        <button
                            onClick={handleSaveSettings}
                            className="w-full px-5 py-2 bg-green-500 text-white rounded-full font-semibold hover:bg-green-600 transition-colors"
                        >
                            Save Settings
                        </button>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Settings;
