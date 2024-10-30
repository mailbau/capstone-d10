"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter, usePathname } from 'next/navigation';

function Header() {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const dropdownRef = useRef(null);
    const notificationRef = useRef(null);
    const router = useRouter();
    const pathname = usePathname();

    const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);
    const toggleNotification = () => setIsNotificationOpen(!isNotificationOpen);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) setIsDropdownOpen(false);
            if (notificationRef.current && !notificationRef.current.contains(event.target)) setIsNotificationOpen(false);
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleLogOut = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    const showFullHeader = pathname !== '/login' && pathname !== '/register' && pathname !== '/about';

    return (
        <header className="flex justify-between items-center px-6 py-3 bg-white shadow-md border-b border-gray-200 w-full">
            <div className="flex items-center gap-3">
                <img loading="lazy" src="/logo.svg" alt="logo" className="w-8 h-8" />
                <h1 className="text-2xl font-semibold text-stone-900">
                    Waste Management Dashboard
                </h1>
            </div>

            {showFullHeader && (
                <nav className="flex items-center gap-6">
                    <ul className="flex gap-6 items-center text-base font-medium text-gray-700">
                        <li>
                            <button onClick={() => router.push('/dashboard')} className="hover:text-blue-600">
                                Dashboard
                            </button>
                        </li>
                        <li>
                            <button onClick={() => router.push('/management')} className="hover:text-blue-600">
                                TPS Management
                            </button>
                        </li>
                    </ul>

                    <div className="relative flex items-center gap-4">
                        <button
                            className="flex items-center justify-center w-10 h-10 bg-gray-100 rounded-full hover:bg-gray-200"
                            aria-label="Notifications"
                            onClick={toggleNotification}
                        >
                            <img loading="lazy" src="/notification.svg" alt="Notification icon" className="w-5 h-5" />
                        </button>

                        {isNotificationOpen && (
                            <div
                                ref={notificationRef}
                                className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg py-2 z-10 transform transition duration-200 ease-out scale-100 opacity-100"
                                style={{ top: '100%' }}
                            >
                                <ul className="text-sm text-gray-700">
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Notification 1</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Notification 2</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Notification 3</li>
                                </ul>
                            </div>
                        )}

                        <button
                            className={`flex items-center justify-center w-10 h-10 bg-gray-100 rounded-full hover:bg-gray-200 transition-transform transform ${isDropdownOpen ? 'rotate-180' : 'rotate-0'}`}
                            aria-label="User profile"
                            onClick={toggleDropdown}
                        >
                            <img loading="lazy" src="/user.svg" alt="User profile icon" className="w-5 h-5 transition-transform transform" />
                        </button>

                        {isDropdownOpen && (
                            <div
                                ref={dropdownRef}
                                className={`absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg py-2 z-10 transform transition-all duration-300 ease-out ${isDropdownOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0'
                                    }`}
                                style={{ top: '100%' }}
                            >
                                <ul className="text-sm text-gray-700">
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => router.push('/profile')}>Profile</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Settings</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Help</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={handleLogOut}>Log Out</li>
                                </ul>
                            </div>
                        )}
                    </div>
                </nav>
            )}
        </header>
    );
}

export default Header;
