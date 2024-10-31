"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter, usePathname } from 'next/navigation';

function Header() {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const dropdownRef = useRef(null);
    const notificationRef = useRef(null);
    const router = useRouter();
    const pathname = usePathname();

    const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);
    const toggleNotification = () => setIsNotificationOpen(!isNotificationOpen);
    const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

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
                    Capstone D-10
                </h1>
            </div>

            {/* Mobile Menu Button */}
            <button
                className="md:hidden flex items-center justify-center w-10 h-10 bg-gray-100 rounded-full hover:bg-gray-200"
                onClick={toggleMobileMenu}
                aria-label="Open mobile menu"
            >
                <img src="/menu.svg" alt="Mobile menu icon" className="w-5 h-5" />
            </button>

            {/* Navigation for Larger Screens */}
            {showFullHeader && (
                <nav className="hidden md:flex items-center gap-6">
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
                                className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg py-2 z-10 transform transition duration-200 ease-out"
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
                                className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg py-2 z-10 transform transition-all duration-300 ease-out"
                                style={{ top: '100%' }}
                            >
                                <ul className="text-sm text-gray-700">
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => router.push('/profile')}>Profile</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => router.push('/settings')}>Settings</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer" onClick={() => router.push('/help')}>Help</li>
                                    <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-red-600" onClick={handleLogOut}>Log Out</li>
                                </ul>
                            </div>
                        )}
                    </div>
                </nav>
            )}

            {/* Mobile Dropdown Menu */}
            {isMobileMenuOpen && showFullHeader && (
                <div className="absolute top-16 left-0 right-0 bg-white shadow-lg rounded-lg z-10 p-4 md:hidden">
                    <ul className="flex flex-col gap-4 text-gray-700">
                        <li>
                            <button onClick={() => { router.push('/dashboard'); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                Dashboard
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { router.push('/management'); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                TPS Management
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { toggleNotification(); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                Notifications
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { router.push('/profile'); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                Profile
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { router.push('/settings'); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                Settings
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { router.push('/help'); setIsMobileMenuOpen(false); }} className="w-full text-left hover:text-blue-600">
                                Help
                            </button>
                        </li>
                        <li>
                            <button onClick={() => { handleLogOut(); setIsMobileMenuOpen(false); }} className="w-full text-left text-red-600 hover:text-red-800">
                                Log Out
                            </button>
                        </li>
                    </ul>
                </div>
            )}
        </header>
    );
}

export default Header;
