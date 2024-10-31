// File: pages/Help.js
"use client";

import React from 'react';
import Header from '../../components/header';
import Footer from '../../components/footer';

function Help() {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex flex-col items-center justify-center flex-grow w-full p-6">
                <div className="flex flex-col items-center w-full max-w-2xl p-6 space-y-6 bg-white rounded-lg shadow-lg">
                    <div className="flex flex-col items-center w-full mb-6">
                        <h2 className="text-3xl font-bold text-gray-800">Help & FAQ</h2>
                        <p className="mt-2 text-gray-500">Find answers to common questions</p>
                    </div>
                    <div className="flex flex-col space-y-4 w-full">
                        <div className="p-4 bg-gray-100 rounded-lg shadow">
                            <h3 className="font-semibold text-gray-800">How do I reset my password?</h3>
                            <p className="text-gray-600 mt-1">Go to Profile Settings, and click on "Edit" to update your password.</p>
                        </div>
                        <div className="p-4 bg-gray-100 rounded-lg shadow">
                            <h3 className="font-semibold text-gray-800">How do I change my email address?</h3>
                            <p className="text-gray-600 mt-1">Navigate to Profile Settings, and update your email in the email field.</p>
                        </div>
                        <div className="p-4 bg-gray-100 rounded-lg shadow">
                            <h3 className="font-semibold text-gray-800">Who do I contact for support?</h3>
                            <p className="text-gray-600 mt-1">For further assistance, please reach out to our support team at support@example.com.</p>
                        </div>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Help;
